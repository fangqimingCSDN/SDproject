#!/bin/bash
for i in {1..1100}
do
sleep 10
# 随机生成文件名
filename=$(date +%s%N)
echo "filename: $filename"

# 创建文件
touch $filename

# 删除文件
rm -f $filename

# 查看内存使用情况
free -m

# 生成脚本文件
scriptname=$(date +%s%N)
echo "scriptname: $scriptname"
cat > $scriptname.sh << EOF
#!/bin/bash

# 随机生成文件名
filename=\$(date +%s%N)
echo "filename: \$filename"

# 创建文件
touch \$filename

# 删除文件
rm -f \$filename
###############################children test####
scriptname1=$(date +%s%N+children)
echo "scriptname1: $scriptname1"
cat > $scriptname1.sh << EOF
#!/bin/bash
# 随机生成文件名
filename=\$(date +%s%N)
echo "filename: \$filename"

# 创建文件
touch \$filename

# 删除文件
rm -f \$filename

# 查看内存使用情况
free -m
###############################children test##############################
scriptname2=$(date +%s%N+children)
echo "scriptname2: $scriptname2"
cat > $scriptname2.sh << EOF
#!/bin/bash
# 随机生成文件名
filename=\$(date +%s%N)
echo "filename: \$filename"

# 创建文件
touch \$filename

# 删除文件
rm -f \$filename

# 查看内存使用情况
free -m
EOF
chmod +x $scriptname2.sh
./$scriptname2.sh
##################children test  end ######################################
rm -f \$scriptname2.sh
EOF
chmod +x $scriptname1.sh
./$scriptname1.sh
rm -f \$scriptname1.sh
##################children test  end ###############
# 查看内存使用情况
free -m
EOF
echo "touch my_$scriptname.sh" >> $scriptname.sh
echo "rm my_$scriptname.sh">> $scriptname.sh
chmod +x $scriptname.sh
./$scriptname.sh
# 删除文件
#rm -f \$scriptname.sh
done