/^# / { 
    var=FILENAME; n=split (var,a,/\//); name=a[n]
    sub(".py","",name)
    $1=""; print "+ ["name"](doc/" name ".md): " $0}