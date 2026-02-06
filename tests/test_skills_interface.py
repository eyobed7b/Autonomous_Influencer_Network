import inspect
import pytest


def test_skills_modules_accept_correct_parameters():
    """Verify that skill modules expose the expected entrypoints and parameter names.

    This defines the interface contract for skills the system expects to call.
    """

    expectations = [
        ("skills.skill_generate_video", "generate_video", ["task"]),
        ("skills.skill_transcribe_audio", "transcribe_audio", ["audio_path", "language"]),
        ("skills.skill_download_youtube", "download_video", ["url", "dest_path"]),
    ]

    for module_path, func_name, params in expectations:
        try:
            module = __import__(module_path, fromlist=[func_name])
        except Exception:
            pytest.fail(f"Missing skill module: {module_path} - implement {func_name}()")

        func = getattr(module, func_name, None)
        assert callable(func), f"{func_name} must be a callable in {module_path}"

        sig = inspect.signature(func)
        for p in params:
            assert p in sig.parameters, f"{func_name} missing required parameter '{p}'"
