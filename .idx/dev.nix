{ pkgs, ... }: {

  # Which nixpkgs channel to use
  channel = "stable-24.05";

  # Packages required for development
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip

    # OCR + PDF support
    pkgs.tesseract
    pkgs.poppler_utils

    # Utilities
    pkgs.git
    pkgs.curl
  ];

  # Environment variables
  env = {
    PYTHONUNBUFFERED = "1";
    TESSERACT_CMD = "${pkgs.tesseract}/bin/tesseract";
    POPPLER_PATH = "${pkgs.poppler_utils}/bin";
  };

  # VS Code / IDX extensions
  idx.extensions = [
    "ms-python.python"
    "ms-python.vscode-pylance"
  ];

  # Enable previews (THIS FIXES THE POPUP)
  idx.previews = {
    enable = true;
    previews = {
      api = {
        command = [
          "bash"
          "-c"
          "uvicorn app:app --host 0.0.0.0 --port $PORT"
        ];
        manager = "web";
      };
    };
  };

  # Workspace lifecycle hooks
  idx.workspace = {

    # Runs once when workspace is created
    onCreate = {
      install-deps = ''
        pip install --upgrade pip
        pip install -r requirements.txt
      '';
    };

    # Runs when workspace starts
    onStart = {
      info = ''
        echo "Workspace ready."
        echo "FastAPI running in IDX preview."
      '';
    };
  };
}
