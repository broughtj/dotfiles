;; -*- lexical-binding: t; -*-
;; Disable package.el
(setq package-enable-at-startup nil)
(setq package--init-file-ensured t)

;; Reduce UI clutter before init
(menu-bar-mode -1)
(tool-bar-mode -1)
(scroll-bar-mode -1)
(setq ring-bell-function 'ignore)

;; Load elpaca directly
;; (defvar elpaca-installer-version 0.6)
;; (defvar elpaca-directory (expand-file-name "elpaca" user-emacs-directory))
;; (defvar elpaca-builds-directory (expand-file-name "builds" elpaca-directory))
;; (defvar elpaca-repos-directory (expand-file-name "repos" elpaca-directory))
;; (defvar elpaca-order '(elpaca-use-package))
;; 
;; (unless (file-exists-p elpaca-directory)
;;   (with-current-buffer
;;       (url-retrieve-synchronously
;;        "https://raw.githubusercontent.com/progfolio/elpaca/main/elpaca-installer.el"
;;        'silent 'inhibit-cookies)
;;     (goto-char (point-max))
;;     (eval-print-last-sexp)))
;; 
;; (load (expand-file-name "elpaca.el" elpaca-directory) nil 'nomessage)
