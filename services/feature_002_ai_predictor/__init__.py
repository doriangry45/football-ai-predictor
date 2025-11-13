import os

# Make this package point to the existing hyphenated feature directory so imports
# like `services.feature_002_ai_predictor.app` resolve to
# `services/feature-002-ai-predictor/app.py` during tests and tooling.
pkg_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'feature-002-ai-predictor'))
if os.path.isdir(pkg_dir):
    __path__.insert(0, pkg_dir)
