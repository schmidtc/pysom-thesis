@Echo visial.exe script for Arcgis
@if not %4 == "true" goto skip
@if not %5 == "#" goto buffer

@Echo no optional parameters passed
@Echo begining visual.exe
Time /T >> Z:\aag\som\bmu.log
Date /T >> Z:\aag\som\bmu.log
@Z:\svn\SOM_PAK\visual.exe -din %1 -cin %2 -dout %3 >> Z:\aag\som\bmu.log
@goto end

:skip
@if not %5 == "#" goto skipbuffer
@Echo vector no skip mode 
@Echo begining visual.exe
Time /T >> Z:\aag\som\bmu.log
Date /T >> Z:\aag\som\bmu.log
@Z:\svn\SOM_PAK\visual.exe -din %1 -cin %2 -dout %3 -noskip >> Z:\aag\som\bmu.log
@goto end

:buffer
@Echo read buffer mode
@Echo begining visual.exe
Time /T >> Z:\aag\som\bmu.log
Date /T >> Z:\aag\som\bmu.log
@Z:\svn\SOM_PAK\visual.exe -din %1 -cin %2 -dout %3 -buffer %5 >> Z:\aag\som\bmu.log
@goto end

:skipbuffer
@Echo vector no skip and read buffer mode
@Echo begining visual.exe
Time /T >> Z:\aag\som\bmu.log
Date /T >> Z:\aag\som\bmu.log
@Z:\svn\SOM_PAK\visual.exe -din %1 -cin %2 -dout %3 -noskip -buffer %5 >> Z:\aag\som\bmu.log
@goto end

:end 
Time /T >> Z:\aag\som\bmu.log
Date /T >> Z:\aag\som\bmu.log
