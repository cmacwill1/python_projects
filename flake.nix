{
  description = "ME581 flake combining latex, python, and notebooks";

  inputs = {
    pythonCore.url = "github:cmacwill1/nixShells?dir=pythonShells/pythonCore";
    pythonBasicPackages.url = "github:cmacwill1/nixShells?dir=pythonShells/pythonBasicPackages";
    pythonNotebook.url = "github:cmacwill1/nixShells?dir=pythonShells/pythonNotebook";
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self,  nixpkgs, ... }@inputs:
  let
    system = "x86_64-linux";

    pkgs = nixpkgs.legacyPackages.${system};
    python = inputs.pythonCore.packages.${system}.default;

    allPythonPackages = inputs.pythonBasicPackages.lib.pythonPackages
                        ++ inputs.pythonNotebook.lib.pythonPackages;
  in
  {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [
        (python.withPackages (pythonPkgs: allPythonPackages))
      ];

  shellHook = ''
    # Create a Jupyter kernel that uses this shell's Python
    KERNEL_DIR="$HOME/.local/share/jupyter/kernels/nix-shell"
    mkdir -p "$KERNEL_DIR"
    cat > "$KERNEL_DIR/kernel.json" <<EOF
    {
      "argv": ["${python.withPackages (pythonPkgs: allPythonPackages)}/bin/python", "-m", "ipykernel_launcher", "-f", "{connection_file}"],
      "display_name": "Python (Nix Shell)",
      "language": "python"
    }
    EOF
    echo "Jupyter kernel 'nix-shell' created/updated"
    echo "Use :MoltenInit nix-shell in Neovim"
  '';
    };
  };
}
