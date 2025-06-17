;; -*- lexical-binding: t; -*-

;; Disable package.el
(setq package-enable-at-startup nil)
(setq package--init-file-ensured t)

;; Reduce UI clutter before init
(menu-bar-mode -1)
(tool-bar-mode -1)
(scroll-bar-mode -1)
(setq ring-bell-function 'ignore)

;; Turn off native compilation for now
(setq native-comp-deferred-compilation nil)

;; Turn off the startup message
(setq inhibit-startup-message t)

