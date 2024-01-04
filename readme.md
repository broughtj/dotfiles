## To Instantiate Nix-Darwin

```{shell}
nix run --extra-experimental-features nix-command --extra-experimental-features flakes nix-darwin -- switch --flake /path/to/flake.nix
```

## To Instantiate Home-Manager

```{shell}
nix run /path/to/flake.nix#homeConfigurations.tjb@Hostname.activationPackage
```


## Home Manager Options


