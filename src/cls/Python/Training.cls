Class Python.Training Extends %Persistent
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
<DataLocation>^Python.TrainingD</DataLocation>
<DefaultData>TrainingDefaultData</DefaultData>
<IdLocation>^Python.TrainingD</IdLocation>
<IndexLocation>^Python.TrainingI</IndexLocation>
<StreamLocation>^Python.TrainingS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
