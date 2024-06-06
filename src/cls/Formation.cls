Class Formation.Formation Extends %Persistent
{

Property Nom As %String;

Property Salle As %String;

Storage Default
{
<Data name="FormationDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Nom</Value>
</Value>
<Value name="3">
<Value>Salle</Value>
</Value>
</Data>
<DataLocation>^Formation.FormationD</DataLocation>
<DefaultData>FormationDefaultData</DefaultData>
<IdLocation>^Formation.FormationD</IdLocation>
<IndexLocation>^Formation.FormationI</IndexLocation>
<StreamLocation>^Formation.FormationS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
