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
  };

  outputs = inputs@{ self, nix-darwin, nixpkgs, home-manager }:
  let
    system = { pkgs, ... }: {
      # List packages installed in system profile. To search by name, run:
      # $ nix-env -qaP | grep wget
      environment.systemPackages =
        [ pkgs.vim
        ];

      # Auto upgrade nix package and the daemon service.
      services.nix-daemon.enable = true;
      # nix.package = pkgs.nix;

      # Necessary for using flakes on this system.
      nix.settings.experimental-features = "nix-command flakes";

      # Create /etc/zshrc that loads the nix-darwin environment.
      programs.zsh.enable = true;  # default shell on catalina
      # programs.fish.enable = true;

      # Set Git commit hash for darwin-version.
      system.configurationRevision = self.rev or self.dirtyRev or null;

      # Used for backwards compatibility, please read the changelog before changing.
      # $ darwin-rebuild changelog
      system.stateVersion = 4;

      # The platform the configuration will be used on.
      nixpkgs.hostPlatform = "aarch64-darwin";

      # This is TJB now rather than autogen stuff
      users.users.tjb.home = "/Users/tjb/";
    };
    home = { pkgs, ... }: {
      home.username = "tjb";
      home.homeDirectory = "/Users/tjb";

      # No touchy, seriously don't ever change this
      home.stateVersion = "23.11";

      programs.home-manager.enable = true;

      # Your stuff here:
    };
  in
  {
    # Build darwin flake using:
    # $ darwin-rebuild build --flake .#simple
    darwinConfigurations."Old-Ben" = nix-darwin.lib.darwinSystem {
      modules = [ system ];
    };

    # Expose the package set, including overlays, for convenience.
    darwinPackages = self.darwinConfigurations."Old-Ben".pkgs;

    homeConfigurations."tjb@Old-Ben" = home-manager.lib.homeManagerConfiguration {
      # Still don't totally understand importing is necessary here, but I haven't found a better way.
      pkgs = import nixpkgs {
        system = "aarch64-darwin";
        config.allowUnfree = true;
      };

      # Specify your home configuration modules here, for example,
      # the path to your home.nix.
      # If you would like to split into multiple files in the future, this is the place to do it.
      modules = [ home ];

      # Optionally use extraSpecialArgs
      # to pass through arguments to home.nix
    };
  };
}