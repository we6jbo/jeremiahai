<?php
declare(strict_types=1);

$base = __DIR__;
$docs = $base . '/documents';
if (!is_dir($docs)) { @mkdir($docs, 0755, true); }

function h($s){ return htmlspecialchars((string)$s, ENT_QUOTES|ENT_SUBSTITUTE, 'UTF-8'); }
function clean_name($s){
    $s = strtolower(trim((string)$s));
    $s = preg_replace('/[^a-z0-9]+/', '-', $s);
    $s = trim($s, '-');
    return $s !== '' ? $s : 'untitled';
}
function disk_used_percent(){
    $total = @disk_total_space('/');
    $free = @disk_free_space('/');
    if (!$total) return null;
    return (($total-$free)/$total)*100.0;
}
function writing_time_policy(){
    $day=(int)date('N');
    $hour=(int)date('G');
    $minute=(int)date('i');
    $mins=$hour*60+$minute;

    if($day>=1 && $day<=5 && $mins>=420 && $mins<660){
        return ['visible'=>true,'time'=>($day===4?'6:30 AM':'7:00 AM')];
    }
    if(($day===1 || $day===2) && $mins>=660 && $mins<870)
        return ['visible'=>false,'time'=>''];
    if(($day===3 || $day===5) && $mins>=660 && $mins<1050)
        return ['visible'=>false,'time'=>''];
    if($day===4 && $mins>=660 && $mins<960)
        return ['visible'=>false,'time'=>''];

    return ['visible'=>true,'time'=>date('g:i A')];
}
function tool_path($names){
    foreach($names as $n){
        $p = trim((string)@shell_exec('command -v '.escapeshellarg($n).' 2>/dev/null'));
        if($p!=='') return $p;
    }
    return null;
}
function analyze_text($text){
    $out=[];
    $tmp=__DIR__.'/.analysis';
    if(!is_dir($tmp)) @mkdir($tmp,0755,true);
    $f=$tmp.'/draft-'.getmypid().'.md';
    file_put_contents($f,$text);

    $coach='/home/jeremiahai/language/analyze.py';
    if(is_file($coach) && is_executable($coach)){
        $cmd='python3 '.escapeshellarg($coach).' '.escapeshellarg($f).' 2>&1';
        $result=trim((string)shell_exec($cmd));
        $out[]="JEREMIAH PI LANGUAGE COACH\n".($result!==''?$result:'The language coach returned no text.');
    } else {
        $out[]="JEREMIAH PI LANGUAGE COACH\n".
            "The custom Pi language coach is unavailable. ".
            "Expected: /home/jeremiahai/language/analyze.py";
    }

    @unlink($f);
    $out[]="WRITING COACH MODE\n".
        "JeremiahAI does not auto-apply fixes. Type the suggested correction yourself, ".
        "then run Analyze / Teach again. Learned Jeremiah-specific rules, Hunspell/Aspell, ".
        "LanguageTool, and Vale are used when available.";
    return implode("\n\n",$out);
}

$selected = isset($_GET['doc']) ? basename((string)$_GET['doc']) : '';
$title=''; $body=''; $revision=0; $message=''; $analysis='';
$author="Jeremiah Burke O'Neal"; $tags=''; $publishDate=''; $filename='';

if($selected!=='' && preg_match('/^[a-z0-9._-]+\.jaiw$/',$selected)){
    $path=$docs.'/'.$selected;
    if(is_file($path)){
        $obj=json_decode((string)file_get_contents($path),true);
        if(is_array($obj)){
            $title=(string)($obj['title']??'');
            $body=(string)($obj['body']??'');
            $revision=(int)($obj['revision']??0);
            $author=(string)($obj['author']??"Jeremiah Burke O'Neal");
            $filename=(string)($obj['filename']??$selected);
            $publishDate=(string)($obj['intended_publish_date']??'');
            $tags=implode(', ',(array)($obj['tags']??[]));
        }
    }
}

if($_SERVER['REQUEST_METHOD']==='POST'){
    $title=trim((string)($_POST['title']??'Untitled'));
    $body=(string)($_POST['body']??'');
    $name=(string)($_POST['filename']??'');
    if(!preg_match('/^[a-z0-9._-]+\.jaiw$/',$name)){
        if(trim($title)==='' && trim($body)===''){
            $message='Please provide a filename before saving a blank draft.';
            $name='';
        } else {
            $basis=trim($title)!=='' ? $title : implode(' ',array_slice(preg_split('/\\s+/',trim($body)),0,8));
            $name=clean_name($basis).'.jaiw';
        }
    }

    if($name!=='' && !isset($_POST['existing_document'])){
        $base=preg_replace('/\.jaiw$/','',$name);
        $candidate=$name;
        $n=2;
        while(is_file($docs.'/'.$candidate)){
            $candidate=$base.'-'.$n.'.jaiw';
            $n++;
        }
        $name=$candidate;
    }

    if(isset($_POST['analyze'])){
        $analysis=analyze_text($body);
        $selected=$name;
    } else {
        $used=disk_used_percent();
        if($used!==null && $used>=50.0){
            $message=sprintf('SAVE REFUSED: Pi disk usage is %.1f%%. Ladybug limit requires usage below 50%%.',$used);
        } else {
            $path=$docs.'/'.$name;
            $oldRev=0;
            if(is_file($path)){
                $old=json_decode((string)file_get_contents($path),true);
                if(is_array($old)) $oldRev=(int)($old['revision']??0);
            }
            $policy=writing_time_policy();
            $tagList=array_values(array_filter(array_map('trim',explode(',',(string)($_POST['tags']??'')))));
            $obj=[
                'format'=>'jeremiahai-writing',
                'format_version'=>1,
                'title'=>$title,
                'filename'=>$name,
                'author'=>"Jeremiah Burke O'Neal",
                'site'=>'j03.page',
                'slug'=>preg_replace('/\.jaiw$/','',$name),
                'tags'=>$tagList,
                'intended_publish_date'=>trim((string)($_POST['publish_date']??'')),
                'revision'=>$oldRev+1,
                'created_at'=>($oldRev===0?gmdate('c'):($old['created_at']??gmdate('c'))),
                'updated_at'=>gmdate('c'),
                'updated_by'=>'pi-8080',
                'source_machine'=>'pi-8080',
                'display_date'=>date('F j, Y'),
                'time_visible'=>$policy['visible'],
                'word_count'=>str_word_count($body),
                'body'=>$body
            ];
            if($policy['visible']) $obj['display_time']=$policy['time'];
            file_put_contents($path,json_encode($obj,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES));
            $selected=$name;
            $revision=$oldRev+1;
            $message='Saved '.$name.' on the Pi.';
        }
    }
}

$list=glob($docs.'/*.jaiw') ?: [];
sort($list);
$used=disk_used_percent();
$coach=(is_file('/home/jeremiahai/language/analyze.py')?'available':'missing');
$hunspell=tool_path(['hunspell']);
$aspell=tool_path(['aspell']);
$vale=tool_path(['vale']);
$lt=tool_path(['languagetool-commandline','languagetool']);
?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>JeremiahAI Writing Lab</title>
<style>
html,body{min-height:100%;overflow:auto} body{font-family:system-ui,sans-serif;margin:0;background:#f4f4f4;color:#222}
header,main{max-width:1100px;margin:auto;padding:16px}
.card{background:#fff;border:1px solid #ccc;border-radius:8px;padding:14px;margin-bottom:14px}
textarea{width:100%;min-height:420px;box-sizing:border-box;font:16px/1.5 ui-monospace,monospace;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere}
input[type=text]{width:100%;box-sizing:border-box;padding:8px}
button{padding:8px 14px;margin-right:6px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;overflow:auto}
.small{font-size:.9em;color:#555}
.warn{border-left:6px solid #777}
</style>
</head>
<body>
<header><h1>JeremiahAI Writing Lab</h1>
<p>Recovery writing workspace for j03.page — documents use <strong>.jaiw</strong>.</p>
<p id="clock"></p></header>
<script>
function writingClockPolicy(d){
  const day=d.getDay(); // Sun=0
  const mins=d.getHours()*60+d.getMinutes();
  let visible=true, t=null;
  if(day>=1 && day<=5 && mins>=420 && mins<660){
    t=(day===4?'6:30 AM':'7:00 AM');
  } else if((day===1||day===2) && mins>=660 && mins<870){
    visible=false;
  } else if((day===3||day===5) && mins>=660 && mins<1050){
    visible=false;
  } else if(day===4 && mins>=660 && mins<960){
    visible=false;
  }
  const date=d.toLocaleDateString(undefined,{weekday:'long',year:'numeric',month:'long',day:'numeric'});
  if(!visible) return date+' — time hidden by JeremiahAI policy';
  if(t===null) t=d.toLocaleTimeString(undefined,{hour:'numeric',minute:'2-digit'});
  return date+' — '+t;
}
function updateClock(){document.getElementById('clock').textContent=writingClockPolicy(new Date());}
setInterval(updateClock,1000); window.addEventListener('load',updateClock);
</script>
<main>
<div class="card">
<strong>Ladybug status:</strong>
Pi disk used: <?=h($used===null?'unknown':sprintf('%.1f%%',$used))?> |
Jeremiah coach: <?=h($coach)?> |
Hunspell: <?=h($hunspell?'available':'not installed')?> |
Aspell: <?=h($aspell?'available':'not installed')?> |
Vale: <?=h($vale?'available':'not installed')?> |
LanguageTool: <?=h($lt?'available':'not installed')?>
<p class="small">Analyze / Teach uses the Jeremiah-specific Pi language coach first. It then uses installed spelling/grammar/style tools on demand. Nothing runs continuously. Saving is refused if Pi disk usage reaches 50%.</p>
</div>

<?php if($message!==''): ?><div class="card warn"><?=h($message)?></div><?php endif; ?>

<div class="card">
<form method="get">
<label>Open document:</label>
<select name="doc">
<option value="">-- choose --</option>
<?php foreach($list as $f): $n=basename($f); ?>
<option value="<?=h($n)?>" <?=$n===$selected?'selected':''?>><?=h($n)?></option>
<?php endforeach; ?>
</select>
<button type="submit">Open</button>
</form>
</div>

<div class="card">
<form method="post">
<?php if($selected!==''): ?><input type="hidden" name="existing_document" value="1"><?php endif; ?>
<label>Author</label>
<input type="text" value="Jeremiah Burke O'Neal" readonly>
<label>Title</label>
<input type="text" name="title" value="<?=h($title)?>">
<label>Filename</label>
<input type="text" name="filename" value="<?=h($selected!==''?$selected:$filename)?>" placeholder="Suggested or chosen filename.jaiw">
<label>Publish date</label>
<input type="text" name="publish_date" value="<?=h($publishDate)?>" placeholder="Optional">
<label>Tags</label>
<input type="text" name="tags" value="<?=h($tags)?>" placeholder="comma-separated">
<p><label>Draft</label></p>
<textarea name="body"><?=h($body)?></textarea>
<p>
<button type="submit" name="save" value="1">Save to Pi</button>
<button type="submit" name="analyze" value="1">Analyze / Teach</button>
</p>
</form>
</div>

<?php if($analysis!==''): ?>
<div class="card">
<h2>Writing Coach</h2>
<pre><?=h($analysis)?></pre>
</div>
<?php endif; ?>

<div class="card">
<h2>Teaching rule</h2>
<p>JeremiahAI should explain spelling, grammar, style, and clarity patterns rather than silently replacing your writing. Revise the sentence yourself, then re-run the check.</p>
</div>
</main>
</body>
</html>
