{
  description = "Dotfiles configuration with nix-darwin and Home Manager for macOS (Apple Silicon)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";

    home-manager.url = "github:nix-community/home-manager";

    nix-darwin.url = "github:LnL7/nix-darwin";
  };

  outputs = { self, nixpkgs, home-manager, nix-darwin }: {
    darwinConfigurations = {
      Frisell = nix-darwin.lib.darwinSystem {
        system = "aarch64-darwin"; # Apple Silicon architecture
        modules = [
          ./darwin-configuration.nix
          home-manager.nixosModules.home-manager
        ];
        specialArgs = { inherit home-manager; };
      };
    };

    homeConfigurations = {
      "tjb@Frisell" = home-manager.lib.homeManagerConfiguration {
        pkgs = import nixpkgs {
          system = "aarch64-darwin";
        };
        modules = [
          ./home.nix
        ];
      };
    };
  };
}
