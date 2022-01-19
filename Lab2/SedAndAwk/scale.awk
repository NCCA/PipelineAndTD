#!/usr/bin/awk -f
# set the counters to zero
BEGIN{
}
# this gets executed per line
{
  if($1 == "v"){
    printf "%s %f %f %f \n", $1,$2*0.5,$3*0.5,$4*0.5 
  }
  else
  {
    print $0
  }
}
# this happens at the end
END{
}