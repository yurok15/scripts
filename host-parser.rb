#!/usr/bin/env ruby

#Get all hosts to string variable
string = File.open('/home/yzhigulskiy/imhosts'){ |file| file.read }

#Covert string to array
array_of_host_names = string.split(" ")


def create_types(variable)
  # Создать массив из типов боксов
  array_of_host_types = []
  for i in variable do
    array_of_host_types << i.split(/\s|\.|-|[0-9]/)[0]
  end
array_of_host_types = array_of_host_types.uniq
return array_of_host_types
end

def assign_hosts_to_type(array_of_host_types, array_of_host_names)
hash = {}
  for b in array_of_host_types do
    hash[b] = []
  end

  for i in array_of_host_names do
    type = i.split(/\s|\.|-|[0-9]/)[0]
    hash[type] << i
  end
  return hash
end

array_of_host_types = create_types(array_of_host_names)
array_of_hosts_and_assigned_types = assign_hosts_to_type(array_of_host_types, array_of_host_names)
#puts array_of_hosts_and_assigned_types

array_of_hosts_and_assigned_types.each do |key, value|
  puts key, value
  puts
end

# 1 Generate ansible inventory
# 2 Generate DC inventory
# 3 Generate cssh host file
