{ pkgs }: {
  # Stable channel
  channel = "stable-24.05";

  # Packages required for development
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip

    # OCR + PDF support
    pkgs.tesseract
    pkgs.poppler_utils

    # Build tools (safe defaults)
    pkgs.git
    pkgs.curl
  ];

  # Environment variables
  env = {
    TESSERACT_CMD = "${pkgs.tesseract}/bin/tesseract";
    POPPLER_PATH = "${pkgs.poppler_utils}/bin";
    PYTHONUNBUFFERED = "1";
  };

  idx = {
    extensions = [
      "ms-python.python"
      "ms-python.vscode-pylance"
    ];

    previews = {
      enable = true;
    };

    workspace = {
      # Run once when workspace is created
      onCreate = {
        install-deps = ''
          pip install --upgrade pip
          pip install -r requirements.txt
        '';
      };

      # Run every time workspace starts
      onStart = {
        start-backend = ''
          echo "Workspace ready. Start backend with:"
          echo "uvicorn app:app --reload"
        '';
      };
    };
  };
}
