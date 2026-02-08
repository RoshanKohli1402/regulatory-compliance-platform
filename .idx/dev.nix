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

    # Build tools
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
      previews = {
        api = {
          command = [
            "bash"
            "-c"
            "uvicorn app:app --host 0.0.0.0 --port $PORT"
          ];
          manager = "web";
          env = {
            PORT = "$PORT";
          };
        };
      };
    };

    workspace = {
      # Runs once when workspace is created
      onCreate = {
        install-deps = ''
          pip install --upgrade pip
          pip install -r requirements.txt
        '';
      };

      # Runs every time workspace starts
      onStart = {
        start-backend = ''
          echo "Workspace ready."
          echo "FastAPI is available in the preview panel."
        '';
      };
    };
  };
}
