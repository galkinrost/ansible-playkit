# ansible-playkit project

- Every file with private information (password, keys, etc) must be started with line:
  ```# -*- vault: true; -*-```

- If Git is used, pre-commit hook (check for encryption) can be installed with command: ansible-playkit hook install
