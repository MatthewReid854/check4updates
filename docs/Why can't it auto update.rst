.. image:: images/logo.png

-------------------------------------

Why can't it auto update?
-------------------------

You may think "why can't *check4updates* perform the update automatically so my users don't have to be prompted?". Updates must be done manually by the user for 3 reasons:

- 1. It is not possible to update a package that is currently in use. If a package calls an update script during its execution, then the update script calls pip and pip will attempt to delete the old installation as part of the update. This causes an error (at least it does in Windows) because the file to be deleted is currently in use. It is possible to update a package using a script but that script can not be called from within the package to be updated.
- 2. It would interrupt the currently executing script. Any self updating script called mid-way through some other parent script will be faced with the difficult job of ensuring the currently executing script's state and variables are not destroyed by the update process. This may be achieveable by ensuring any update is only performed when the currently running script is finished executing, though Python usually doesn't work this way without some complex threading of subprocesses.
- 3. It would be a security vulnerability for the Python Software Foundation to allow the creation of scripts that can self update in the background without seeking the user's permission. If this was possible it could enable a malicious developer to introduce code on the user's system without their knowledge.

