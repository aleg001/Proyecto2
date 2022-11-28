from math import pi, tan


class InterseccionXD:
    def __init__(self, distance, point, normal):
        self.distance = distance
        self.point = point
        self.normal = normal


class Sphere(object):
    def __init__(self, center, radio, material):
        self.center = center
        self.radio = radio
        self.material = material

    def intersectRay(self, origen, direccion):
        L = self.center - origen
        Tca = L @ direccion
        lenght = L.LenghtValue()

        d2 = lenght**2 - Tca**2

        if d2 > self.radio**2:
            return None

        Thc = (self.radio**2 - d2) ** 0.5
        firstT = Tca - Thc
        secondT = Tca + Thc

        if firstT < 0:
            firstT = secondT

        if firstT < 0:
            return None

        impacto = origen + direccion * firstT
        normalizado = (impacto - self.center).Normalizando()
        return InterseccionXD(firstT, impacto, normalizado)


class Materiales(object):
    def __init__(self, defuse, albedo, spec):
        self.defuse = defuse
        self.albedo = albedo
        self.spec = spec


class Plane(object):
    def __init__(self, center, w, l, material):
        self.material = material
        self.center = center
        self.l = l
        self.w = w

    def intersectRay(self, origin, direction):
        sumatoriaRealizada = self.center.y + origin.y
        sumatoriaRealizada = -(sumatoriaRealizada)
        d = sumatoriaRealizada / direction.y
        tempD = direction * d
        impact = origin + tempD
        biggerX = self.center.x + self.w / 2
        lesserX = self.center.x - self.w / 2
        biggerZ = self.center.z + self.l / 2
        lesserZ = self.center.z - self.l / 2

        if (
            d <= 0
            or impact.x > biggerX
            or impact.x < lesserX
            or impact.z > biggerZ
            or impact.z < lesserZ
        ):
            return None

        return InterseccionXD(distance=d, point=impact, normal=V3(0, 1, 0))


class Luz:
    def __init__(self, posicion, intensidad, color):
        self.posicion = posicion
        self.intensidad = intensidad
        self.color = color


class V3(object):
    def __init__(self, x, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, siguienteAr):
        tempSum = self.x + siguienteAr.x
        tempSum2 = self.y + siguienteAr.y
        tempSum3 = self.z + siguienteAr.z
        finalVector = V3(tempSum, tempSum2, tempSum3)
        return finalVector

    def __sub__(self, siguienteAr):
        firstSub = self.x - siguienteAr.x
        secondSub = self.y - siguienteAr.y
        thirdSub = self.z - siguienteAr.z
        resultVector = V3(firstSub, secondSub, thirdSub)
        return resultVector

    def __mul__(self, siguienteAr):
        if type(siguienteAr) == int or type(siguienteAr) == float:
            resultadoVar1 = V3(
                self.x * siguienteAr, self.y * siguienteAr, self.z * siguienteAr
            )
            return resultadoVar1

        resultadoVar = V3(
            self.y * siguienteAr.z - self.z * siguienteAr.y,
            self.z * siguienteAr.x - self.x * siguienteAr.z,
            self.x * siguienteAr.y - self.y * siguienteAr.x,
        )
        return resultadoVar

    def __matmul__(self, siguienteAr):
        tempVar1 = self.x * siguienteAr.x
        tempVar2 = self.y * siguienteAr.y
        tempVar3 = self.z * siguienteAr.z
        Result = tempVar1 + tempVar2 + tempVar3
        return Result

    def LenghtValue(self):
        return (self.z**2 + self.y**2 + self.x**2) ** (1 / 2)

    def Normalizando(self):
        try:
            return self * (1 / self.LenghtValue())
        except:
            return V3(-1, -1, -1)


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __mul__(self, o):
        r = self.r
        b = self.b
        g = self.g
        if type(o) == int or type(o) == float:
            r *= o
            g *= o
            b *= o
        else:
            r *= o.r
            g *= o.g
            b *= o.b

        r = min(255, max(r, 0))
        g = min(255, max(g, 0))
        b = min(255, max(b, 0))

        return Color(r, g, b)

    def __add__(self, o):
        r = self.r
        b = self.b
        g = self.g
        if type(o) == int or type(o) == float:
            r += o
            g += o
            b += o

        else:
            r += o.r
            g += o.g
            b += o.b
        return Color(r, g, b)

    def toBytes(self):
        return bytes([int(self.b), int(self.g), int(self.r)])


def Reflexiones(Inter, aNormalizar):
    tempValue = Inter - aNormalizar * 2
    tempValue2 = aNormalizar @ Inter
    result = tempValue * tempValue2
    resultNormaliced = result.Normalizando()
    return resultNormaliced
