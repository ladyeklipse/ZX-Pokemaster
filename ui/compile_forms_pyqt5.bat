for /r %%f in (*.qrc) do pyrcc5 -o %%~nf_rc.py %%~nf.qrc
for /r %%f in (*.ui) do pyuic5 -o %%~nf.py %%~nf.ui