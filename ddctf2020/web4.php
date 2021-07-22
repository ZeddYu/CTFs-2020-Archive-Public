

<?php
error_reporting(0);

class MyClass
{
    var $kw0ng;
    var $flag;

    public function __wakeup()
    {
        $this->kw0ng = 1;
    }

    public function get_flag()
    {
        return system('find /FlagNeverFall ' . escapeshellcmd($this->flag));
    }
}

class Prompter
{   
    protected  $hint;
    public function execute($value)
    {
        include($value);
    }

    public function __invoke()
    {
        if(preg_match("/gopher|http|file|ftp|https|dict|zlib|zip|bzip2|data|glob|phar|ssh2|rar|ogg|expect|\.\.|\.\//i", $this->hint))
        {
            die("Don't Do That!");
        }
        $this->execute($this->hint);
    }
}

class Display
{
    public $contents;
    public $page;
    public function __construct($file='/hint/hint.php')
    {
        $this->contents = $file;
        echo "Welcome to DDCTF 2020, Have fun!<br/><br/>";
    }
    public function __toString()
    {
        return $this->contents();
    }

    public function __wakeup()
    {
        $this->page->contents = "POP me! I can give you some hints!";
        unset($this->page->cont);
    }
}

class Repeater
{
    private $cont;
    public $content;
    public function __construct()
    {
        $this->content = array();
    }

    public function __unset($key)
    {
        $func = $this->content;
        return $func();
    }
}

class Info
{
    function __construct()
    {
        eval('phpinfo();');
    }

}

$show = new Display();
$bullet = $_GET['bullet'];

if(!isset($bullet))
{
    highlight_file(__FILE__);
    die("Give Me Something!");
}else if($bullet == 'phpinfo')
{
    $infos = new Info();
}else
{
    $obstacle = new stdClass;
    $mc = new MyClass();
    $mc->flag = "MyClass's flag said, Overwrite Me If You Can!";
    @unserialize($bullet);
    echo $mc->get_flag();
}

Give Me Something!
Welcome to DDCTF 2020, Have fun!