BEGIN       { yes=no=0       }	
            { m="."          }	
/True/      { yes += gsub("True","") ; m = "+" } 
/False/     { no  += gsub("False",""); m = "X" } 
            { printf m       } 
! (NR % 50) { print ""}
END         { print "\ntests passed",yes,"failed",no }
