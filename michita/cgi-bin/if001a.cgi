#!/usr/local/bin/perl

#=====================================================================
# ����
#=====================================================================
#   ̾    ��: WwwMail Ver3.27
#   �ǽ�����: 2008ǯ1��14��
#   �� �� ��: ���㡹
#   ��    ��: �ե꡼���եȡʻ��ѡ����Ѥ���鷺���ѡ���¤��ή�ѡ������۲ġ�
#   �� �� ��: http://tohoho.wakusei.ne.jp/

#=====================================================================
# �������ޥ���
#=====================================================================
# �� perl�Υѥ�̾
#    ���Υե��������Ƭ�Σ��Ԥ򡢤��ʤ������Ѥ��륵���С��˥��󥹥ȡ�
#    �뤵�줿 perl ���ޥ�ɤΥѥ�̾�˱������ѹ����Ƥ����������㤨�С�
#    �䤬�������Ƥ��� BIGLOBE �Ǥϡ�#!/usr/local/bin/perl �Ȥʤ�ޤ���
#    ���ʤ����ϡ��ץ��Х����䥵���Фδ����Ԥˤ��䤤��碌����������
#   ��#!�פ����ˤϡ���ʸ������Ԥ�¾��ʸ�����Ϥ���ʤ��褦�ˤ��Ƥ���������

# �� ������᡼�륢�ɥ쥹
#    $mailto = 'abc@xxx.yyy.zzz'; �Τ褦�ˤ��ʤ��Υ᡼�륢�ɥ쥹��
#    �񤭴����Ƥ���������
$mailto = 'infoproc@ayu.ics.keio.ac.jp';

# �� ���֥�������(��̾)
#    ���������᡼��Υ��֥������Ȥ���ꤷ�Ƥ���������
$subject = '[infoproc]080502';

# �� �᡼���������ޥ��
#    Web�����С���UNIX�ξ���sendmail���ޥ�ɡ�Windows�Ϥξ���BLATJ.EXE
#    ���ޥ�ɤΥѥ�̾������$mailcmd = 'C:\BLATJ\BLATJ.EXE'; �ʤɡˤ��Ƥ�
#    �����������Υ��ޥ�ɤ�¸�ߤ��ʤ����ϡ�WwwMail ��ư��ޤ��󡣤ޤ���
#    ¸�ߤ��Ƥ��Ƥ⡢�᡼�����������꤬�Ԥ��Ƥ��ʤ���礬����ޤ����ܺ�
#    �ϥץ��Х����䥵���С��δ����Ԥˤ��䤤��碌����������
$mailcmd = '/usr/lib/sendmail';

# �� ������̥�å�����(�إå�)
#    <<END_OF_DATA �� END_OF_DATA �δ֤򹥤ߤˤ��碌���ѹ����Ƥ���������
$header = <<END_OF_DATA;
<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=Shift_JIS">
<title>restult</title>
</head>
<body>
<h1>Finish</h1>
<hr>
<hr>
END_OF_DATA

# �� ������̥�å�����(�եå�)
#    <<END_OF_DATA �� END_OF_DATA �δ֤򹥤ߤˤ��碌���ѹ����Ƥ���������
$footer = <<END_OF_DATA;
</body>
</html>
END_OF_DATA

#====================================================================
# ���ʿ��ǵ�ǽ��
#====================================================================
# �᡼�����������ޤ�ư��ʤ����ˡ�
# http://��/��/wwwmail.cgi?test �η����ǸƤӽФ��Ƥ���������
if ($ENV{'REQUEST_METHOD'} eq "GET") {
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>WwwMail</title>\n";
	print "</head>\n";
	print "<body>\n";
	print "<p>CGI is OK</p>\n";
	unless (-f $mailcmd) {
		print "<p>No $mailcmd</p>\n";
	}
	unless (-x $mailcmd) {
		print "<p>Cannot execute $mailcmd</p>\n";
	}
	unless (-f "jcode.pl") {
		print "<p>No jcode.pl</p>\n";
	}
	unless (-f "mimew.pl") {
		print "<p>No mimew.pl</p>\n";
	}
	print "</body>\n";
	print "</html>\n";
	exit 0;
}

#====================================================================
# ����
#====================================================================

#
# �饤�֥��θƤӽФ�
#
require "jcode.pl";
require "mimew.pl";

#
# �����ͤ��ɤ߼��
#
if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $query_string, $ENV{'CONTENT_LENGTH'});
	@a = split(/&/, $query_string);
	foreach $x (@a) {
		($name, $value) = split(/=/, $x);
		$name =~ tr/+/ /;
		$name =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		&jcode'convert(*name, "jis");
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		$value =~ s/\r\n/\n/g;
		&jcode'convert(*value, "jis");
		if ($FORM{$name} eq "") {
			$FORM{$name} = $value;
			$FORM[$cnt++] = $name;
		} else {
			$FORM{$name} .= (" " . $value);
		}
	}
}

#
# EMAIL������ʥ᡼�뤢�ɤ줹���ɤ���Ƚ�Ǥ���
#
if ($FORM{'EMAIL'} =~ /^[-_\.a-zA-Z0-9]+\@[-_\.a-zA-Z0-9]+$/) {
	$mailfrom = $FORM{'EMAIL'};
}

#
# �᡼��إå����������
#
{
	&jcode'convert(*subject, "jis");
	$mailhead = "";
	$mailhead .= "Content-Type: text/plain; charset=\"iso-2022-jp\"\n";
	$mailhead .= "Content-Transfer-Encoding: 7bit\n";
	$mailhead .= "MIME-Version: 1.0\n";
	$mailhead .= "To: $mailto\n";
	if ($mailfrom) {
		$mailhead .= "From: $FORM{'EMAIL'}\n";
#		$mailhead .= "Cc: $FORM{'EMAIL'}\n";
	} else {
		$mailhead .= "From: $mailto\n";
	}
	$mailhead .= "Subject: $subject\n";
	$mailhead .= "\n";
}

#
# �᡼��ܥǥ����������
#
{
	for ($i = 0; $i < $cnt; $i++) {
		$mailbody .= "$FORM[$i] = $FORM{$FORM[$i]}\n";
	}

	$mailbody .=  "ADDR        = [ $ENV{'REMOTE_ADDR'} ]\n";
        $mailbody .= "test_ADDR   = [ $ENV{'HTTP_X_FORWARDED_FOR'} ]\n";
        $mailbody .= "test2_ADDR  = [ $ENV{'HTTP_FORWARDED'} ]\n";
        $mailbody .= "USER        = [ $ENV{'REMOTE_USER'} ]\n";
        $mailbody .= "USER2       = [ $ENV{'REMOTE_IDENT'} ]\n";
        if ($ENV{'REMOTE_HOST'} ne $ENV{'REMOTE_ADDR'}) {
                $mailbody .= "HOST  = [ $ENV{'REMOTE_HOST'} ]\n";
        }
        $mailbody .= "AGENT       = [ $ENV{'HTTP_USER_AGENT'} ]\n";
        # print(OUT "REFER = [ $referer ]\n");
        if ($reffile && (!$my_url || ($reffile !~ /$my_url/))) {
                $mailbody .= "FROM  = [ $reffile ]\n";
        }
        $mailbody .= "VIA         = [ $ENV{'HTTP_VIA'} ]\n"; # lin
        $mailbody .= "REF         = [ $ENV{'HTTP_REFERER'} ]\n"; # lin


	# "." �ΤߤιԤ� ". " ���Ѵ����롣
	# 2�󷫤��֤��ʤ��ȡ�2��Ϣ³�� "." �ΤߤιԤ��б��Ǥ��ʤ�
	# "." �� ".." ���Ѵ��������������Ū�����������������ơ�
	# "." �� ". " ���Ѵ����롣
	$mailbody =~ s/(^|\n)\.(\n|$)/$1. $2/g;
	$mailbody =~ s/(^|\n)\.(\n|$)/$1. $2/g;
}

#
# �᡼�����������
#
if ($mailcmd =~ /sendmail/) {
	unless (open(OUT, "| $mailcmd -t")) {
		&errexit("cannot send (1)");
	}
	unless (print OUT &mimeencode($mailhead)) {
		&errexit("cannot send (2)");
	}
	unless (print OUT $mailbody) {
		&errexit("cannot send (3)");
	}
	close(OUT);
} elsif ($mailcmd =~ /BLAT/i) {
	&jcode'convert(*subject, "sjis");
	$cmd = "$mailcmd";
	$cmd .= " -";
	$cmd .= " -t $mailto";
	$cmd .= " -s \"$subject\"";
	if ($mailfrom) {
		$cmd .= " -c $mailfrom";
		$cmd .= " -f $mailfrom";
	}
	unless (open(OUT, "| $cmd > NUL:")) {
		&errexit("cannot send (4)");
	}
	&jcode'convert(*mailbody, "sjis");
	unless (print OUT $mailbody) {
		&errexit("cannot send (5)");
	}
	&jcode'convert(*mailbody, "jis");
	close(OUT);
} else {
	&errexit("No $mailcmd");
}

#
# �֥饦�����̤�������̤�񤭽Ф�
#
{
	&jcode'convert(*header, "euc");
	&jcode'convert(*footer, "euc");

	$mail = $mailhead . $mailbody;
	&jcode'convert(*mail, "euc");
	$mail =~ s/&/&amp;/g;
	$mail =~ s/"/&quot;/g;
	$mail =~ s/</&lt;/g;
	$mail =~ s/>/&gt;/g;
	$mail =~ s/\n/<BR>/g;
	&jcode'convert(*mail, "euc");

	print "Content-type: text/html\n";
	print "\n";
	print "$header\n";
	print "������<a href=\"http://www.ayu.ics.keio.ac.jp/~michita/Joho2008/080502.doc\">�����򱦥���å�����</a>�������Ʊ�½��Υե��������¸��\n";
#	print "$mail\n";
	print "$footer\n";
}

#
# ���顼��å���������Ϥ��ƽ�λ
#
sub errexit {
	local($err) = @_;
	local($msg);

	$msg  = "Content-type: text/html\n";
	$msg .= "\n";
	$msg .= "<html>\n";
	$msg .= "<head>\n";
	$msg .= "<meta http-equiv=\"Content-type\" content=\"text/html; charset=Shift_JIS\">\n";
	$msg .= "<title>Result</title>\n";
	$msg .= "</head>\n";
	$msg .= "<body>\n";
	$msg .= "<h1>Result</h1>\n";
	$msg .= "<hr>\n";
	$msg .= "<p>$err</p>\n";
	$msg .= "<hr>\n";
	$msg .= "</body>\n";
	$msg .= "</html>\n";

	&jcode'convert(*msg, "euc");

	print $msg;

	exit(0);
}