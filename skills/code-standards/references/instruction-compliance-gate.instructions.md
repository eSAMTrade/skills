## Mandatory instruction-compliance gate

Before modifying code:

1. Identify all project instructions relevant to the proposed design.
2. If the proposed design conflicts with any explicit instruction, DO NOT implement it.
3. Either choose a compliant design or stop and ask the user for permission to violate the rule.
4. Have the author or reviewer audit every proposed boolean flag, mode enum, constructor option, strategy, factory, wrapper, sentinel value, and every callback, lambda,
   functional interface, or callable type alias used as a dependency or extension boundary. A delegating task owner verifies the audit evidence before edits.
5. Passing tests does not override a design instruction.

Before finishing:

1. Have an author or reviewer inspect the actual diff within the assigned scope and compare every new abstraction and public API change against the relevant project instructions.
2. Report the inspection evidence and any intentional exception explicitly; a delegating task owner verifies that evidence. Never silently accept an exception.
