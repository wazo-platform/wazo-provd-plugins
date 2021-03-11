# Limitations

Here is a list of what is known to be non-working or malfunctioning on this DECT system:

* **Phonebook**: the phonebook URL is too long for what the firmware accepts as a parameter.
  Therefore, the phonebook does not work.
* **Timezone** : provd is not able to determine the country from a timezone. It is not possible
  to define the country of the DECT and the daylight-savings time changes.
