{
  description = "Example Darwin system flake";

  # There are sets, except their definition of a set is wrong and bad. They really
  # mean a dictionary or map (sets of key-value pairs).
  #
  # When they write:
  # inputs.nixpkgs.url = 1;
  # it is shorthand for
  # { inputs = { nixpkgs = { url = 1; }}}.
  #
  # There are also functions. They look like this:
  #
  # x: x + 2.
  #
  # Most of the time though, the functions will take sets as inputs, and they 
  # use pattern-matching (or destructuring in Python lingo) syntax to destructure
  # the set arguments. For example,
  #
  # { self, nix-darwin, nixpkgs }: self.foo
  #
  # would take a set with the keys `self`, `nix-darwin`, `nixpkgs` and then 
  # return the value of `foo` in the dictionary `self.`
  #
  # Functional programmers don't like parenthesis, so to call a function f on an input x looks like
  #
  # f x
  #
  # Parenthesis are instead used to indicate calling order when expresssions are complex. For example
  #
  # f (g x)
  #
  # is notation for first calling g on x and then calling f on the result.
  #
  # There's some syntax for `let` bindings, and there's a fancy thing for `with`,
  # but other than that, that's basically the whole thing.
  #
  # There is also the inherit syntax, which just helps reduce boilerplate. The syntax
  #
  # { inherit foo; }
  #
  # is just sugar for
  #
  # { foo = foo; }
  #
  # The whole point of this is that we functionally describe package dependencies
  # without any side-effects. No implicit dependencies is the whole goal.
  #
  # TODO:
  # - Nix modules (https://nixos.wiki/wiki/NixOS_modules)
  #
  # Articles:
  #
  # Article describing flakes and specifically the output schema:
  # https://nixos.wiki/wiki/Flakes#Flake_schema
  #
  #

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    nix-darwin.url = "github:LnL7/nix-darwin";
    nix-darwin.inputs.nixpkgs.follows = "nixpkgs";

    home-manager.url = "github:nix-community/home-manager";
    home-manager.inputs.nixpkgs.follows = "nixpkgs";

    emacs-overlay.url = "github:nix-community/emacs-overlay";
    emacs-overlay.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs@{ self, nixpkgs, nix-darwin, home-manager, emacs-overlay }:
    let
      emacsOverlay = (pkgs: package: 
        (pkgs.emacsWithPackagesFromUsePackage {
          inherit package;
          config = ./emacs.el;
          defaultInitFile = true;
          alwaysEnsure = true;
        })
      );
    in
    rec {
      nixosModules = rec {
        darwinSystem = { pkgs, ... }: {
          # Set Git commit hash for darwin-version.
          system.configurationRevision = self.rev or self.dirtyRev or null;
          # Used for backwards compatibility, please read the changelog before changing.
          # $ darwin-rebuild changelog
          system.stateVersion = 4;
          # Auto upgrade nix package and the daemon service.
          services.nix-daemon.enable = true;
          # Necessary for using flakes on this system.
          nix.settings.experimental-features = "nix-command flakes";

          # List packages installed in system profile. To search by name, run:
          # $ nix-env -qaP | grep wget
          environment.systemPackages = [ pkgs.vim ];

          programs.zsh.enable = true;

          homebrew.enable = true;
          homebrew.casks = [
            "dropbox"
            "fantastical"
            "google-chrome"
            "google-drive"
            "mathpix-snipping-tool"
            "modular"
            "slack"
            "spotify"
            "todoist"
            "visual-studio-code"
            "vlc"
            "warp"
            "zoom"
            "zotero"
          ];
        };
        oldBen = { ... }: {
          imports = [ darwinSystem ];

          # The platform the configuration will be used on.
          nixpkgs.hostPlatform = "aarch64-darwin";

          # This is TJB now rather than autogen stuff
          users.users.tjb.home = "/Users/tjb/";
        };
        cooder = { pkgs, ...}: {
          imports = [ darwinSystem ];

          nixpkgs.hostPlatform = "aarch64-darwin";

          users.users.tylerbrough.home = "/Users/tylerbrough";
        };
        home = { config, pkgs, ... }: {
          imports = [ emacsConfiguration ];

          # No touchy, seriously don't ever change this
          home.stateVersion = "23.11";
          programs.home-manager.enable = true;

          # home.username = "tjb";
          home.homeDirectory = "/Users/${config.home.username}";

          home.packages = with pkgs; [
            tree 
            ripgrep
          ];

          programs.git = {
            enable = true;
            userName = "Tyler Brough";
            userEmail = "broughtj@gmail.com";
            extraConfig.init.defaultBranch = "main";
          };

          programs.emacs.package = emacsOverlay pkgs pkgs.emacs29-macport;
          home.sessionVariables.EDITOR = "emacsclient";
        };
        homeOldBen = { ... }: {
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
      # Build darwin flake using:
      # $ darwin-rebuild build --flake .#simple
      darwinConfigurations."Old-Ben" = nix-darwin.lib.darwinSystem {
        modules = [ nixosModules.oldBen ];
      };
      homeConfigurations."tjb@Old-Ben" = home-manager.lib.homeManagerConfiguration {
        pkgs = import nixpkgs {
          system = "aarch64-darwin";
          config.allowUnfree = true;
        };
        modules = [ nixosModules.homeOldBen ];
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
