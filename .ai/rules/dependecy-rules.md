# Dependency Rules

The architecture enforces strict dependency direction: 

```
Presentation → Application → Domain
                    ↓
             Infrastructure
```

## Rules

 * Domain Layer
   - Must not depend on any other layer
   - Defines interfaces (Ports) only

 * Infrastructure Layer
   - Must not depend on any other layer
   - Entity Framework Core, Database and Entity Mappings are placed here
   - Drivers for other database are placed here
   - Proxies and Facade implementations for external services are placed here
 
 * Application Layer
   - Depends on `Domain` and `Infrastructure`
   - Implements Domain interfaces (Adapters)

 * Presentation Layer
   - Depends only on `Application`
   - Must not contain business logic

# Additional Constraints

 * No circular dependencies
 * All external systems must be accessed via Domain interfaces
 * Business logic must remain inside the Domain layer only
 * Infrastructure must be replaceable without impacting Domain or Application
