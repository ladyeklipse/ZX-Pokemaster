for /r %%f in (*.qrc) do pyrcc4 -py3 -o %%~nf_rc.py %%~nf.qrc
for /r %%f in (*.ui) do pyuic4 -o %%~nf.py %%~nf.ui
