# Directory to store encrypted SSH private key files

- Unencrypted key name must match inventory name and ends with ".pem" extension
- Key files must be encrypted with command: ansible-playkit vault encryptkey <file>
- Valid encrypted file name example: <inventory_name>.pem.encrypted
