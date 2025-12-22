---
title: "PlantUML Diagrams"
---

If you are a user who wants to publish pages to Confluence, you should install the package [markdown-to-confluence](https://pypi.org/project/markdown-to-confluence/) from PyPI. If you are a developer who wants to contribute, you should clone the repository [md2conf](https://github.com/hunyadi/md2conf) from GitHub.

[PlantUML](https://plantuml.com/) is an open-source tool that allows you to create diagrams from a plain text language. You can include PlantUML diagrams in your documents to create visual representations of systems, processes, and relationships.

## Sequence Diagram

Sequence diagrams show how objects interact with each other over time. They are useful for modeling the dynamic behavior of a system and understanding message flows between components.

```plantuml
@startuml
actor User
participant "Web App" as Web
participant "API Server" as API
database "Database" as DB

User -> Web: Login request
Web -> API: Authenticate(username, password)
API -> DB: Query user
DB --> API: User data
API --> Web: Auth token
Web --> User: Login successful
@enduml
```

## Class Diagram

Class diagrams visualize the structure of a system by showing its classes, attributes, methods, and relationships. They are essential for object-oriented design.

```plantuml
@startuml
abstract class Animal {
  +name: String
  +age: int
  +makeSound(): void
}

class Dog {
  +breed: String
  +bark(): void
  +makeSound(): void
}

class Cat {
  +color: String
  +meow(): void
  +makeSound(): void
}

Animal <|-- Dog
Animal <|-- Cat
@enduml
```

## Component Diagram

Component diagrams illustrate the organization and dependencies among software components, helping to visualize system architecture.

```plantuml
@startuml
package "Frontend" {
  [React App] as React
  [State Manager] as Redux
}

package "Backend" {
  [REST API] as API
  [Business Logic] as Logic
  [Data Access] as DAO
}

database "PostgreSQL" as DB

React --> Redux
React --> API
API --> Logic
Logic --> DAO
DAO --> DB
@enduml
```

## Theme Customization Examples

PlantUML supports various built-in themes that change the visual appearance of diagrams. You can apply themes globally using the `--plantuml-theme` CLI option or per-diagram using YAML front-matter.

### Themed Class Diagram (bluegray)

This example demonstrates a class diagram with the **bluegray theme** applied via YAML front-matter. The theme provides a modern, professional appearance with blue-gray colors.

**Configuration**: Uses `theme: bluegray` in the diagram's YAML front-matter.

![Themed Class Diagram](figure/themed_class.puml)

### Activity Diagram with cerulean-outline Theme

This activity diagram uses the **cerulean-outline theme**, which provides a clean, outlined style with cerulean blue accents. This theme works well for flowcharts and activity diagrams.

**Configuration**: Can be applied with `--plantuml-theme cerulean-outline` CLI option.

```plantuml
@startuml
!theme cerulean-outline
start
:User opens app;
if (Is logged in?) then (yes)
  :Load dashboard;
  :Display user data;
else (no)
  :Show login screen;
  :User enters credentials;
  :Authenticate;
  if (Valid credentials?) then (yes)
    :Create session;
    :Load dashboard;
  else (no)
    :Show error message;
    stop
  endif
endif
:User interacts with app;
stop
@enduml
```

## Skinparam Customization Examples

Skinparams allow fine-grained control over diagram styling by setting specific visual properties. You can apply skinparams globally using `--plantuml-skinparam key=value` CLI option or per-diagram using YAML front-matter.

### Styled Sequence Diagram

This sequence diagram demonstrates custom styling with **skinparams** for background color and arrow thickness.

**Configuration**: Uses `skinparams` in YAML front-matter with `backgroundColor` and `sequenceArrowThickness` settings.

![Styled Sequence Diagram](figure/styled_sequence.puml)

### Component Diagram with Custom Colors

This component diagram uses skinparams to customize colors for packages, components, and connections.

**Configuration**: Can be applied with multiple `--plantuml-skinparam` options like `--plantuml-skinparam packageBackgroundColor=#E8F5E9 --plantuml-skinparam componentBackgroundColor=#BBDEFB`.

```plantuml
@startuml
skinparam packageBackgroundColor #E8F5E9
skinparam componentBackgroundColor #BBDEFB
skinparam componentBorderColor #1976D2
skinparam arrow {
  Color #388E3C
  Thickness 2
}

package "Mobile App" {
  component [UI Layer]
  component [Business Logic]
}

package "Cloud Services" {
  component [API Gateway]
  component [Microservices]
}

[UI Layer] --> [Business Logic]
[Business Logic] --> [API Gateway]
[API Gateway] --> [Microservices]
@enduml
```

## Include File Examples

Include files allow you to define reusable PlantUML configurations, styles, or standard elements that can be shared across multiple diagrams. You can specify includes globally using `--plantuml-include path/to/file.puml` CLI option or per-diagram using YAML front-matter.

### Use Case Diagram with Standard Elements

This use case diagram demonstrates using an include file that might define standard actors, styles, or common use cases used across your documentation.

**Configuration**: Can be applied with `--plantuml-include figure/plantuml-common.puml` CLI option or via YAML front-matter `includes: [figure/plantuml-common.puml]`.

```plantuml
@startuml
left to right direction
actor "Customer" as customer
actor "Administrator" as admin

rectangle "E-commerce System" {
  usecase "Browse Products" as UC1
  usecase "Add to Cart" as UC2
  usecase "Checkout" as UC3
  usecase "Manage Inventory" as UC4
  usecase "View Reports" as UC5
  usecase "Manage Users" as UC6
}

customer --> UC1
customer --> UC2
customer --> UC3
admin --> UC4
admin --> UC5
admin --> UC6

UC3 ..> UC2 : <<includes>>
@enduml
```

## State Diagram with Combined Configuration

This state diagram demonstrates using **multiple configuration options together**: theme, skinparams, and custom styling for a cohesive appearance.

**Configuration**: Combine `--plantuml-theme` with multiple `--plantuml-skinparam` options for comprehensive customization.

```plantuml
@startuml
!theme toy
skinparam state {
  BackgroundColor #FFF9C4
  BorderColor #F57C00
  ArrowColor #E65100
}

[*] --> Idle
Idle --> Processing : Start
Processing --> Validating : Data received
Validating --> Processing : Invalid data
Validating --> Complete : Valid data
Complete --> [*]
Processing --> Error : Exception
Error --> Idle : Retry
Error --> [*] : Give up
@enduml
```

## Deployment Diagram

Deployment diagrams show the physical architecture of a system, including hardware nodes and the software components deployed on them.

**Configuration**: Uses default styling; can be customized with any of the above options.

```plantuml
@startuml
node "Client Browser" {
  [Web Interface]
}

node "Application Server" {
  [Web Server]
  [Application Logic]
}

node "Database Server" {
  database "MySQL" {
    [User Data]
    [Transaction Logs]
  }
}

node "Cache Server" {
  [Redis Cache]
}

[Web Interface] --> [Web Server] : HTTPS
[Web Server] --> [Application Logic]
[Application Logic] --> [User Data] : JDBC
[Application Logic] --> [Redis Cache] : TCP
@enduml
```
