(setq package-enable-at-startup nil)
(setq use-package-ensure-function 'ignore)
(setq package-archives nil)

(setq use-package-always-ensure t)
(eval-when-compile (require 'use-package))
;; Required for ~:bind~ to work later
(require 'bind-key)


(when (fboundp 'menu-bar-mode) (menu-bar-mode 0))
(when (fboundp 'tool-bar-mode) (tool-bar-mode 0))
(when (fboundp 'scroll-bar-mode) (scroll-bar-mode 0))
(setq visible-bell t)
(setq display-line-numbers-type 'visual)
(global-display-line-numbers-mode)

(setq-default indent-tabs-mode nil)


(use-package evil
 :init
 (setq evil-want-keybinding nil)
 :custom
 (evil-undo-system 'undo-redo)
 :config
 (evil-mode 1))

(use-package evil-collection
 :after evil
 :custom (evil-want-keybinding nil)
 :init
 (evil-collection-init))

(use-package vertico
  :init
  (vertico-mode))

(use-package marginalia
  :init
  (marginalia-mode))

(use-package consult)

(use-package orderless
  :custom
  (completion-styles '(orderless basic))
  (completion-category-overrides '((file (styles basic partial-completion)))))

(use-package which-key
  :config (which-key-mode 1))

(use-package company
  :custom
  (company-idle-delay 0.1)
  :bind
  (:map company-active-map
	("C-n" . company-select-next)
	("C-p" . company-select-previous))
  :init
  (global-company-mode))

(use-package yasnippet
  :config
  (yas-reload-all)
  (add-hook 'prog-mode-hook 'yas-minor-mode)
  (add-hook 'text-mode-hook 'yas-minor-mode))

(use-package standard-themes)

(use-package modus-themes)

(use-package ef-themes 
  :init
  (load-theme 'ef-melissa-dark t))

(use-package nix-mode
  :mode "\\.nix\\'")

(use-package envrc
  :config
  (envrc-global-mode))

(use-package magit)


;; TODO: This is copied from broughjt. Understand it better!
(setq org-src-preserve-indentation nil
      org-edit-src-content-indentation 0
      org-confirm-babel-evaluate nil
      org-babel-load-languages
        '((emacs-lisp . t)
          (shell . t)
          (python . t))
      org-latex-compiler "lualatex"
      org-latex-create-formula-image-program 'dvisvgm
      org-preview-latex-image-directory temporary-file-directory
      org-latex-packages-alist '(("" "bussproofs" t))
      org-startup-with-latex-preview t
      org-startup-with-inline-images t
      org-agenda-span 14)
(add-hook 'org-mode-hook 'turn-on-auto-fill)

(use-package org-ql)
(use-package org-roam-ql)

(use-package org-modern
  :hook (org-mode . org-modern-mode))

(use-package org-fragtog
  :hook (org-mode . org-fragtog-mode))


;; Okay, let's do this! Org-Roam Setup
(use-package org-roam
  :custom
  (org-roam-v2-ack t)
  (org-directory "~/Dropbox/org")
  (org-roam-directory "~/Dropbox/orgroam/notes")
  (org-roam-dailies-directory "~/Dropbox/orgroam/dailies")
  (org-cite-global-bibliography '("~/Dropbox/orgroam/notes/biblio.bib"))
  (org-roam-capture-templates
   '(("d" "default" plain
       "%?" :target
       (file+head "${slug}.org" "#+title: ${title}\n")
       :unnarrowed t)))
   :bind (("C-c n l" . org-roam-buffer-toggle)
	  ("C-c n f" . org-roam-node-find)
	  ("C-c n i" . org-roam-node-insert)
	  ("C-c n t" . org-roam-dailies-capture-today)
	  ("C-c n a" . org-agenda)
	  ;; ("C-c n b" . org-iswitchb)
	  )
   :config
   (require 'oc-basic)
   (org-roam-setup))



;;(use-package org-roam
;;  :custom
;;  (org-roam-v2-ack t)
;;  (org-directory "~/share")
;;  (org-roam-directory "~/share/notes")
;;  (org-roam-dailies-directory "journals/")
;;  (org-cite-global-bibliography '("~/share/notes/citations.bib"))
;;  (org-roam-capture-templates
;;   '(("d" "default" plain
;;      "%?" :target
;;      (file+head "pages/${slug}.org" "#+title: ${title}\n")
;;      :unnarrowed t)))
;;  ;; (org-agenda-files '("~/share/notes" "~/share/notes/daily" "~/share/org"))
;;  ;; (org-roam-dailies-capture-templates
;;   ;; '(("d" "default" entry
;;      ;; "* %?"
;;      ;; :target (file+head "%<%Y-%m-%d>.org"
;;                         ;; "#+title: %<%Y-%m-%d>\n\n"))))
;;  :bind (("C-c n l" . org-roam-buffer-toggle)
;;         ("C-c n f" . org-roam-node-find)
;;         ("C-c n i" . org-roam-node-insert)
;;         ;; ("C-c n t" . org-roam-dailies-capture-today)
;;         ;; ("C-c n a" . org-agenda)
;;         ;; ("C-c n b" . org-iswitchb)
;;         )
;;  :config
;;  (require 'oc-basic)
;;  (org-roam-setup))
