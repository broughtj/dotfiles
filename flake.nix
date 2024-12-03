{
  description = "Dotfiles configuration with nix-darwin and Home Manager for macOS (Apple Silicon)";

  inputs = {
    # Nixpkgs for packages
    nixpkgs.url = "github:NixOS/nixpkgs";

    # Home Manager
    home-manager.url = "github:nix-community/home-manager";

    # nix-darwin
    nix-darwin.url = "github:LnL7/nix-darwin";
  };

  outputs = { self, nixpkgs, home-manager, nix-darwin }: {
    darwinConfigurations = {
      # Replace 'Hostname' with your macOS hostname
      Hostname = nix-darwin.lib.darwinSystem {
        system = "aarch64-darwin";
        modules = [
          ./darwin-configuration.nix # Nix-darwin configuration file
          home-manager.nixosModules.home-manager
        ];
        specialArgs = { inherit home-manager; };
      };
    };

    homeConfigurations = {
      # Replace 'tjb@Hostname' with your desired identifier
      "tjb@Hostname" = home-manager.lib.homeManagerConfiguration {
        pkgs = import nixpkgs {
          system = "aarch64-darwin";
        };
        modules = [
          ./home.nix # Home Manager configuration file
        ];
      };
    };
  };
}
