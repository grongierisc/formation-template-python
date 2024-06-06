/// 
Class Formation.BP.Main Extends Ens.BusinessProcessBPL
{

/// BPL Definition
XData BPL [ XMLNamespace = "http://www.intersystems.com/bpl" ]
{
<process language='objectscript' request='Ens.Request' response='Ens.Response' height='2000' width='2000' >
<sequence xend='200' yend='700' >
<call name='gfdsg' target='Python.HttpBO' async='1' xpos='200' ypos='250' >
<request type='Ens.Request' />
</call>
<if name='fgdsg' condition='1' xpos='200' ypos='350' xend='200' yend='600' >
<true>
<empty xpos='470' ypos='500' />
</true>
<false>
<code languageOverride='objectscript' xpos='200' ypos='500' />
</false>
</if>
</sequence>
</process>
}

Storage Default
{
<Type>%Storage.Persistent</Type>
}

}

