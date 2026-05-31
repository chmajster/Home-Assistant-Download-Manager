"""Regression tests for routes and URL safety."""

from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from app import create_app
from app.services.file_service import FileService
from app.services.job_manager import JobManager
from app.services.youtube_service import YouTubeService, YouTubeServiceError


class ApplicationTestCase(unittest.TestCase):
    """Exercise behavior that must keep working behind Home Assistant Ingress."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        settings = SimpleNamespace(
            download_dir=root / "downloads",
            jobs_dir=root / "jobs",
            history_file=root / "jobs" / "history.json",
            max_concurrent_jobs=2,
            update_ytdlp_on_start=False,
            allow_external_port=False,
            external_port=8099,
            debug=False,
            preferred_format="best",
            secret_key="test-secret",
        )
        with patch("app.AppConfig.load", return_value=settings):
            self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_healthcheck(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_ingress_prefix_is_used_for_generated_links(self) -> None:
        response = self.client.get(
            "/", headers={"X-Ingress-Path": "/api/hassio_ingress/token"}
        )
        body = response.get_data(as_text=True)
        self.assertIn("/api/hassio_ingress/token/static/css/style.css", body)
        self.assertIn("/api/hassio_ingress/token/analyze", body)

    def test_empty_job_api(self) -> None:
        response = self.client.get("/api/jobs")
        self.assertEqual(response.get_json(), {"jobs": []})

    def test_managed_file_can_be_downloaded(self) -> None:
        downloads = self.app.extensions["file_service"].download_dir
        expected = downloads / "example.txt"
        expected.write_text("ok", encoding="utf-8")
        response = self.client.get("/downloaded/example.txt")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_data(as_text=True), "ok")
        finally:
            response.close()


class YouTubeUrlTestCase(unittest.TestCase):
    """Keep extractor input limited to known public YouTube hosts."""

    def test_supported_url_is_normalized(self) -> None:
        url = YouTubeService.validate_url(
            "HTTPS://WWW.YOUTUBE.COM/watch?v=abc#fragment"
        )
        self.assertEqual(url, "https://www.youtube.com/watch?v=abc")

    def test_non_youtube_domain_is_rejected(self) -> None:
        with self.assertRaises(YouTubeServiceError):
            YouTubeService.validate_url("https://example.com/watch?v=abc")

    def test_file_scheme_is_rejected(self) -> None:
        with self.assertRaises(YouTubeServiceError):
            YouTubeService.validate_url("file:///etc/passwd")

    def test_youtube_subdomain_confusion_is_rejected(self) -> None:
        with self.assertRaises(YouTubeServiceError):
            YouTubeService.validate_url("https://youtube.com.example.org/watch?v=abc")

    def test_youtube_redirect_endpoint_is_rejected(self) -> None:
        with self.assertRaises(YouTubeServiceError):
            YouTubeService.validate_url(
                "https://www.youtube.com/redirect?q=https://example.com"
            )


class FakeYouTubeService:
    """Deterministic extractor stand-in for JobManager tests."""

    def __init__(self, download_dir: Path) -> None:
        self.download_dir = download_dir

    validate_url = staticmethod(YouTubeService.validate_url)
    format_selection = staticmethod(YouTubeService.format_selection)

    def download(self, **kwargs):
        target = self.download_dir / "example.mp4"
        target.write_text("media", encoding="utf-8")
        kwargs["progress_hook"](
            {
                "status": "downloading",
                "downloaded_bytes": 50,
                "total_bytes": 100,
                "speed": 1024,
                "eta": 3,
            }
        )
        kwargs["progress_hook"]({"status": "finished", "filename": str(target)})
        return [target]

    def live_command(self, url: str) -> list[str]:
        return ["/venv/bin/python", "-m", "yt_dlp", url]


class JobManagerTestCase(unittest.TestCase):
    """Exercise queue completion and duplicate-live protection."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.download_dir = root / "downloads"
        self.download_dir.mkdir()
        self.files = FileService(self.download_dir, root / "jobs" / "history.json")
        self.manager = JobManager(
            FakeYouTubeService(self.download_dir), self.files, max_concurrent_jobs=1
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_regular_download_completes_and_is_recorded(self) -> None:
        job = self.manager.start_download("https://youtu.be/abc", "Example", "best")
        completed = self._wait_for_status(job.job_id, "completed")
        self.assertEqual(completed.progress, 100.0)
        self.assertEqual(completed.output_file, "example.mp4")
        self.assertEqual(self.files.history()[0]["title"], "Example")

    def test_duplicate_queued_live_is_rejected(self) -> None:
        self.manager._slots.acquire()
        try:
            job = self.manager.start_live("https://youtu.be/live", "Live")
            with self.assertRaises(YouTubeServiceError):
                self.manager.start_live("https://youtu.be/live", "Live")
            stopped = self.manager.stop_live(job.job_id)
            self.assertEqual(stopped.status, "stopped")
        finally:
            self.manager._slots.release()

    def _wait_for_status(self, job_id: str, expected: str):
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            job = self.manager.get_job(job_id)
            if job.status == expected:
                return job
            time.sleep(0.01)
        self.fail(f"Zadanie {job_id} nie osiągnęło stanu {expected}.")


if __name__ == "__main__":
    unittest.main()
