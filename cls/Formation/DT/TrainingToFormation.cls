Class Formation.DT.TrainingToFormation Extends Ens.DataTransformDTL [ DependsOn = (Formation.Training, Formation.Formation) ]
{

Parameter IGNOREMISSINGSOURCE = 1;

Parameter REPORTERRORS = 1;

Parameter TREATEMPTYREPEATINGFIELDASNULL = 0;

XData DTL [ XMLNamespace = "http://www.intersystems.com/dtl" ]
{
<transform sourceClass='Formation.Training' targetClass='Formation.Formation' create='new' language='objectscript' >
<assign value='source.Name_"titi"' property='target.Nom' action='set' />
<assign value='source.Room_"titi"' property='target.Salle' action='set' />
</transform>
}

}

