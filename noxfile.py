import nox
import os
import shutil
import glob

# Try to use uv as the default backend for much faster environment creation
nox.options.default_venv_backend = "uv"

@nox.session(python=["3.13"])
def tests(session):
    """Run the test suite."""
    # Install dependencies required for testing
    session.install("pytest", "pynmea2")
    # Install the package itself
    session.install("-e", ".")
    
    # Run the tests
    session.run("pytest", "tests/")

@nox.session(python=["3.13"])
def build(session):
    """Verify that the package builds and installs correctly."""
    # Clean up the dist directory if it exists
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        
    # Use uv to build the source and wheel distributions
    # We use external=True because uv is a global command in this environment
    session.run("uv", "build", external=True)
    
    # Verify the wheel was created
    wheels = glob.glob("dist/*.whl")
    if not wheels:
        session.error("Build failed: No wheel file found in dist/ directory.")
        
    # Test installing the built wheel in this isolated nox environment
    session.install(wheels[0])
    
    # Verify we can import the package successfully
    session.run("python", "-c", "import nwfsc_nmea; print('Built wheel imported successfully!')")
