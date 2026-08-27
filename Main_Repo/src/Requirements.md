# REQUIREMENTS

## Setup
1. Double click on MidnightWatchCert.pfx (This file gives permissions to the browser to actually be allowed to download and execute properly)

2. A popup will appear asking what place to install it to. Choose LOCAL MACHINE.

3. Accept the prompt to allow changes to the device

4. Press next (Don't change the file name)

5. Enter the password MidnightWatchPass##

6. Tick no other boxes and press next

7. Select "Place all certificates in the following store"

8. Click "Browse"

9. Select "Trusted Root Certification Authorities"

10. Click "Next"

11. Click "Finish"

Repeat the above step, instead selecting "Trusted Publishers" instead of "Trusted Root Certification Authorities"

That concludes the setup for the backend. Simply doubleclick the MSIX installer and follow the prompts on screen.

### Note
This browser runs only on WINDOWS. There are variants for Linux and MacOS but considering they are both executable files and no one will be testing those versions, they have not been included for simplicity's sake.

The certificate setup is complex because microsoft dislikes convenient installations of this manner when they aren't directly certified by an authorisation company. This requires the browser to either have legal standing and pass a code review by microsoft, deploying to their store and becoming a public app, or otherwise a purchased certificate which costs upwards of $500 dollars. 

Since neither option is feasible for the browser, this is the only available method for proper access.
