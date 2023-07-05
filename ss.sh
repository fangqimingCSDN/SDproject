#!/bin/bash
for i in {1..1100}
do
sleep 10
# ��������ļ���
filename=$(date +%s%N)
echo "filename: $filename"

# �����ļ�
touch $filename

# ɾ���ļ�
rm -f $filename

# �鿴�ڴ�ʹ�����
free -m

# ���ɽű��ļ�
scriptname=$(date +%s%N)
echo "scriptname: $scriptname"
cat > $scriptname.sh << EOF
#!/bin/bash

# ��������ļ���
filename=\$(date +%s%N)
echo "filename: \$filename"

# �����ļ�
touch \$filename

# ɾ���ļ�
rm -f \$filename
###############################children test####
scriptname1=$(date +%s%N+children)
echo "scriptname1: $scriptname1"
cat > $scriptname1.sh << EOF
#!/bin/bash
# ��������ļ���
filename=\$(date +%s%N)
echo "filename: \$filename"

# �����ļ�
touch \$filename

# ɾ���ļ�
rm -f \$filename

# �鿴�ڴ�ʹ�����
free -m
###############################children test##############################
scriptname2=$(date +%s%N+children)
echo "scriptname2: $scriptname2"
cat > $scriptname2.sh << EOF
#!/bin/bash
# ��������ļ���
filename=\$(date +%s%N)
echo "filename: \$filename"

# �����ļ�
touch \$filename

# ɾ���ļ�
rm -f \$filename

# �鿴�ڴ�ʹ�����
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
# �鿴�ڴ�ʹ�����
free -m
EOF
echo "touch my_$scriptname.sh" >> $scriptname.sh
echo "rm my_$scriptname.sh">> $scriptname.sh
chmod +x $scriptname.sh
./$scriptname.sh
# ɾ���ļ�
#rm -f \$scriptname.sh
done