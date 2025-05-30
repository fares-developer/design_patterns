# 📐 Patrones de Diseño en Programación Orientada a Objetos

[![Licencia MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pull Requests Bienvenidos](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/faresuclm/design-patterns/pulls)
[![Última Actualización](https://img.shields.io/github/last-commit/faresuclm/design-patterns)](https://github.com/faresuclm/design-patterns/commits/main)

---

## 🎯 Resumen

Este repositorio constituye una exploración concisa y práctica de los patrones de diseño esenciales dentro del paradigma de la Programación Orientada a Objetos (POO). Cada patrón se presenta con una definición clara de su propósito, directrices estratégicas para su aplicación y ejemplos concretos que facilitan una comprensión profunda y una implementación efectiva en escenarios del mundo real.

---

## 🧩 Patrones de Diseño Implementados

## 🛠️ Factory Method

**Objetivo:** Define una interfaz para la creación de objetos, delegando la decisión de la clase concreta a las subclases. Este enfoque encapsula la lógica de instanciación, promoviendo un diseño flexible y altamente reutilizable.

### Aplicación Estratégica:

- Cuando una clase no puede prever el tipo exacto de objetos que necesita instanciar.
- Para permitir que las subclases especifiquen los tipos de objetos a crear.
- Para simplificar la creación de objetos complejos, minimizando el acoplamiento a implementaciones concretas.

### Arquitectura:
![Diagrama de Estructura del Patrón Factory Method](pictures/factory-method.png)

### Implementación Concreta:
En este proyecto, el patrón Factory Method se ejemplifica mediante la generación dinámica de elementos en un entorno de mapa. Se define un `Creator` abstracto para la creación de elementos, con implementaciones especializadas como `CreatorB` para la instanciación de bombas y `CreatorBlind` para la creación de blindaje.

![Ejemplo de Implementación del Patrón Factory Method](pictures/factory-method-ex.png)