## To Instantiate Nix-Darwin

```{shell}
nix run --extra-experimental-features nix-command --extra-experimental-features flakes nix-darwin -- switch --flake /path/to/flake.nix
```

## To Instantiate Home-Manager

```{shell}
nix run /path/to/flake.nix#homeConfigurations.tjb@Hostname.activationPackage
```


## Regular Commands

To `swtich` to the new configuration after `home-manager` has been updated.

```{shell}
home-manager switch --show-trace --flake /path/to/flake.nix
```

To `switch` to the new configuration after `darwin` system has been updated.

```{shell}
darwin-rebuild switch --show-trace --flake /path/to/flake.nix
```

To check to see if changes made to a flake are proper. 

```{shell}
nix flake check --all-systems
```

__NB:__ Just the `/path/to/the/dir` and not the file itself (just the basedir)


