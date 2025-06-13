{
  description = "Example Darwin system flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    nix-darwin.url = "github:LnL7/nix-darwin";
    nix-darwin.inputs.nixpkgs.follows = "nixpkgs";

    home-manager.url = "github:nix-community/home-manager";
    home-manager.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, nix-darwin, home-manager }:
    let
      system = "x86_64-darwin"; # or "aarch64-darwin" if you are on an M1 Mac
      pkgs = import nixpkgs { inherit system; };
      home = home-manager.lib.homeManagerConfiguration {
        pkgs = pkgs;
        modules = [ ./home.nix ];
      };
    in {
      nixosModules = {
        frisell = { ... }: {
          imports = [ home ];

          home-manager.useGlobalPkgs = true;
          home-manager.useUserPackages = true;

          home-manager.enable = true;

          home.homeDirectory = "/Users/${config.home.username}";

          home.packages = with pkgs; [
            djvu2pdf
            direnv
            nushell
            pandoc
            ripgrep
            tree
            imagemagick # Added imagemagick here
          ];

          programs.fish.enable = true;

          programs.git = {
            enable = true;
            userName = "Tyler Brough";
            userEmail = "broughtj@gmail.com";
            extraConfig.init.defaultBranch = "main";
          };

          programs.emacs.package = emacsOverlay pkgs pkgs.emacs29-macport;
          home.sessionVariables.EDITOR = "emacsclient";
        };
        homeFrisell = { ... }: {
          imports = [ home ];

          home.username = "tjb";
        };
        homeCooder = { ... }: {
          imports = [ home ];

          home.username = "tylerbrough";
        };
        emacsConfiguration = { pkgs, ... }: {
          nixpkgs.overlays = with emacs-overlay.overlays; [ emacs package ];

          programs.emacs.enable = true;
        };
      };
      darwinConfigurations."Frisell" = nix-darwin.lib.darwinSystem {
        modules = [ nixosModules.frisell ];
      };
      homeConfigurations."tjb@Frisell" = home-manager.lib.homeManagerConfiguration {
        pkgs = import nixpkgs {
          system = "aarch64-darwin";
          config.allowUnfree = true;
        };
        modules = [ nixosModules.homeFrisell ];
      };
      darwinConfigurations."Cooder" = nix-darwin.lib.darwinSystem {
        modules = [ nixosModules.cooder ];
      };
      homeConfigurations."tylerbrough@Cooder" = home-manager.lib.homeManagerConfiguration {
        pkgs = import nixpkgs {
          system = "aarch64-darwin";
          config.allowUnfree = true;
        };
        modules = [ nixosModules.homeCooder ];
      };
    };
}
