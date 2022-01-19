#!/usr/bin/awk -f
# set the counters to zero
BEGIN{
  count = 0
  limit=ARGV[1]
  ARGV[1] = ""  
}
# this gets executed per line
{
  if($1 == "f" && (count % limit) == 1){
    count=0;
  }
  else
  {
    count++;
    print $0
  }
}
# this happens at the end
END{
}