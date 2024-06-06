Class Formation.Training Extends %Persistent
{

Property Name As %String;

Property Room As %String;

Storage Default
{
<Data name="TrainingDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Name</Value>
</Value>
<Value name="3">
<Value>Room</Value>
</Value>
</Data>
<DataLocation>^Formation.TrainingD</DataLocation>
<DefaultData>TrainingDefaultData</DefaultData>
<IdLocation>^Formation.TrainingD</IdLocation>
<IndexLocation>^Formation.TrainingI</IndexLocation>
<StreamLocation>^Formation.TrainingS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
