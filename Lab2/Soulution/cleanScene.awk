#!/usr/bin/awk -f

BEGIN{
  array_index=0; # index into the input file
  light_array_index=0; # index into light array
  red_count=0;
  green_count=0;
  blue_count=0;
  white_count=0;
}
# This is per line processing
{
  # copy the input file into an array we will process at the end
  array[++array_index]=$0;
  # find the line number of the pointLight
  if ( $2 == "pointLight") 
  {
    # store line number of light in the original file
    light_index[++light_array_index]=NR;
  }
}

function get_colour_name(current_line,array)
{
  # Now find what Colour we have this is simple for the scene as we only
  # have Red,Green,Blue and White. Note NR the number of records, but we only look 
  # until we find the ".cl" for the colour of the light
  for(i=current_line; i<NR; ++i)
  {
    # index will return a positive value if string is found
    if (index(array[i],".cl") !=0)
    {
      if(index(array[i],"1 0 0")!=0)
      {
        light_colour="Red" red_count++; 
      }
      else if (index(array[i],"0 1 0")!=0)
      {
        light_colour="Green" green_count++;
      }
      else if (index(array[i],"0 0 1")!=0)
      {
        light_colour="Blue" blue_count++;
      }
      else if (index(array[i],"1 1 1")!=0)
      {
        light_colour="White" white_count++;
      }
      break;
    }
  }
  return light_colour;
}

END{
    # now we have prepared our data process
    # current_line is the index array we need the number in it
    for (l in light_index)
    {
      current_line=light_index[l];
      split(array[current_line],line," ")
      name=substr(line[4], 2, length(line[4])-2);
      parent=substr(line[6], 1, length(line[6])-1)

      light_colour=get_colour_name(current_line,array)
      # now replace with new name
      gsub(name,"Light" light_colour,array[current_line])
      # now search whole file to replace name in the array. 
      # Obviously this is a log(N) complexity :-( !
      for(i in array)
      {
        if (index(array[i],name) !=0)
        {   
          gsub(name,"Light" light_colour,array[i]);
        }
      }
    }
    # finally we have finished the scene so dump the output
    for(i=0; i<NR; ++i)
    {
       print array[i];
    }
}