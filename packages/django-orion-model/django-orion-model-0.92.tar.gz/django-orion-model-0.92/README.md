A Django App to manage a [Fiware Orion ](https://github.com/telefonicaid/fiware-orion) context broker entities as Django Model Objects.
## Install

In order to intall  simply use pip

```
pip install django_orion_model
```

## Usage

Simply add django_orion_model to your settings.py:

```python
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
    ...
'django_orion_model',
    ...
]

ORION_URL = "https://yourorion:1234"
ORION_SCOPE = "/desiredscope"
ORION_EXPIRATION = 200 // living time of local values
```

To define a Entity Model simply define a class in your models.py Using OrionEntity as Class father and use Orion fields to properties expected to live in the context broker.

```python
from django_orion_model import OrionEntityi

class WasteManagementStage(OrionEntity):
    name = OrionCharField("name", max_length=1024, blank=True)
    description = OrionTextField("description", max_length=1024, blank=True)
```

Available Field types for Orion Context ContextBroker: 

 * OrionCharField
 * OrionTextField
 * OrionFloatField
 * OrionDateTimeField

An orion entity have a Default Field to manage Communication With Orion:

  * context_broker(ForeingKey-ContextBroker): The Orion Context ContextBroker that manages the entity
  * service_path(ForeingKey-Scope): The service-path  where the entity lies.
  * orion_id(CharField): The ID of the entity in Orion.
  * type(CharField): The type of the entity in Orion.
  * data(JSONField): A local repository of the last known values of the entity.
  * updated(ArrayField-CharField): The name of the Orion field updates since las connection.
  * expiration(DateTimeField): The time when the local data is considered obsolete.
  * status(CharField): A predefined text that indicates the communication. Expected values:
    * OK Everything is OK and up to date
    * OFFLINE Set to Disable communication to Orion
    * MISSING Indicates that the Entity not exist in Orion
    * CREATING Set to Create the entity into Orion. 
    * CREATED Indicates that the entity is created but is values are not yet pulled from Orion(Transitory)
    * PENDING_WRITING Indicates that the entity is performing a push to Orion(Transitory).
    * PENDING_READING Indicates that the entity is performing a pull to Orion(Transitory).
    * AWAIT_REFRESH The pull has failed and the entity is expecting a new opportunity to retry.
    * AWAIT_REWRITING The push has failed and the entity is expecting a new opportunity to retry.
  * error(TextField): IF the connection have a problem the Orion response is stored here.
    
## Entity Behaivour

The entity is expected to pull values from Orion after its creation, when an orion attributes is read and expiration time is up, before saving to database and after values are updated to orion. 
The entity is expected to push  values to Orion after a Orion values is Set.

Some status Values forces Some behavior: 

  * OFFLINE Set to Disable communication to Orion
  * CREATING Set to Create the entity into Orion. 
 
----

This library is partially funded  by the [Waste4Think proyect](http://waste4think.eu/) that  has received funding from the European Union’s [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) research and innovation program under grant agreement 688995.
The dissemination of results herein reflects only the author’s view and the European Commission is not responsible for any use that may be made of the information it contains.

