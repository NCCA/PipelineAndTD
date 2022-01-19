#!/usr/bin/awk -f
# set the counters to zero
BEGIN{
  verts=0;
  normals=0;
  uv=0;
  faces=0;
}
# this gets executed per line
{
  if($1 == "v"){verts++;}
  else if($1 == "vn"){normals++;}
  else if($1 == "vt"){uv++;}
  else if($1 == "f"){faces++;}
}
# this happens at the end
END{
  print "Faces ",faces;
  print "verts ",verts;
  print "UV's ",uv;
  print "normals ",normals;
}