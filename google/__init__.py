"""Package initializer for local `google` stub used in tests.

This allows `import google.generativeai` to resolve to the local stub
module during development and CI when the real `google-generativeai`
package is not installed.
"""

__all__ = ["generativeai"]
# Minimal google package placeholder for local testing
__all__ = ["generativeai"]
