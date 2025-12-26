"""
Central exception definitions for SCORM processing
"""


class ScormProcessingError(Exception):
    """
    Base exception for all SCORM-related errors.
    Catch this if you want to handle all SCORM failures generically.
    """
    pass


class ScormValidationError(ScormProcessingError):
    """
    Raised when ZIP or imsmanifest.xml validation fails.
    This is a permanent failure (should usually go to DLQ).
    """
    def __init__(self, errors):
        message = f"SCORM validation failed: {errors}"
        super().__init__(message)
        self.errors = errors


class UnsafeZipError(ScormProcessingError):
    """
    Raised when ZIP contains unsafe paths (zip-slip attack).
    Permanent failure.
    """
    pass


class AlfrescoDownloadError(ScormProcessingError):
    """
    Raised when content download from Alfresco fails.
    Transient in most cases (retryable).
    """
    pass


class AlfrescoUploadError(ScormProcessingError):
    """
    Raised when upload to Alfresco fails.
    Usually retryable.
    """
    pass
