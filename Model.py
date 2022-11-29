from math import acos, atan2, pi, tan
import struct


def ProductoCruz(primerValor, segundoValor):
    return (
        primerValor.y * segundoValor.z - primerValor.z * segundoValor.y,
        primerValor.z * segundoValor.x - primerValor.x * segundoValor.z,
        primerValor.x * segundoValor.y - primerValor.y * segundoValor.x,
    )


def CoordenadasBari(A, B, C, P):
    cx, cy, cz = ProductoCruz(
        V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )
    if abs(cz) < 1:
        return -1, -1, -1
    u = cx / cz
    v = cy / cz
    sumaTemp = u + v
    w = 1 - sumaTemp

    return (w, v, u)


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
    def __init__(self, defuse, albedo, spec, refractiveI=0):
        self.defuse = defuse
        self.albedo = albedo
        self.spec = spec
        self.refractiveI = refractiveI


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


# 5 puntos por envmap
class Envmap(object):
    def __init__(self, path) -> None:
        self.path = path
        self.open1()

    def open1(self):
        with open(self.path, "rb") as file:
            file.seek(10)
            hSize = struct.unpack("=l", file.read(4))[0]
            file.seek(18)
            self.w = struct.unpack("=l", file.read(4))[0]
            self.h = struct.unpack("=l", file.read(4))[0]
            file.seek(hSize)

            self.pixels = []
            for y in range(self.h):
                self.pixels.append([])
                for x in range(self.w):
                    b = ord(file.read(1))
                    g = ord(file.read(1))
                    r = ord(file.read(1))
                    self.pixels[y].append(Color(r, g, b))

    def ObtenerColoracion(self, dir):
        nm = dir.Normalizando()
        x = round(((atan2(nm.z, nm.x) / (2 * pi)) + 0.5) * self.w)
        y = -1 * round((acos((-1 * nm.y)) / pi) * self.h)

        x -= 1 if (x > 0) else 0
        y -= 1 if (y > 0) else 0

        return self.pixels[y][x]


# 30 puntos: Figura diferente a esfera, cubo, rectangulo, plano
class Triangle(object):
    def __init__(self, arrayVectors, material):
        self.Vector = arrayVectors
        self.material = material

    def Lado(self, a, b, c, origen, dir):
        multip = (b - a) * (c - a)
        direccionRayo = multip @ dir

        if direccionRayo < 0.00000001:
            return None

        ValordeD = multip @ a

        Taro = multip @ origen + ValordeD
        DivididoDireccion = Taro / direccionRayo

        if DivididoDireccion < 0:
            return None
        valorP = origen + (dir * DivididoDireccion)
        a1, b1, c1 = CoordenadasBari(a, b, c, valorP)

        if a1 < 0 or b1 < 0 or c1 < 0:
            return None
        else:
            return InterseccionXD(DivididoDireccion, valorP, multip.Normalizando())

    def intersectRay(self, org, dire):
        a, b, c, d = self.Vector
        lados = [
            self.Lado(a, c, b, org, dire),
            self.Lado(a, b, d, org, dire),
            self.Lado(a, d, b, org, dire),
            self.Lado(b, c, d, org, dire),
        ]
        inter = None
        t = float("inf")
        for i in lados:
            if i is not None:
                if i.distance < t:
                    t = i.distance
                    inter = i
        if inter is None:
            return None

        return InterseccionXD(inter.distance, inter.point, inter.normal)


class Disco(object):
    def __init__(self, center, radioGrande, radioPequenio, material):
        self.center = center
        self.radioGrande = radioGrande
        self.radioPequenio = radioPequenio
        self.material = material

    def intersectRay(self, orig, dir):
        L = self.center - orig
        Tca = L @ dir
        lenght = L.LenghtValue()

        d2 = lenght**2 - Tca**2

        if d2 > self.radioGrande:
            return None

        if d2 < self.radioPequenio:
            return None

        Thc = (self.radioGrande**2 - d2**2) ** 0.5
        firstT = Tca - Thc
        secondT = Tca + Thc

        if firstT < 0:
            firstT = secondT

        if firstT < 0:
            return None

        impacto = orig + dir * firstT
        normalizado = (impacto - self.center).Normalizando()
        return InterseccionXD(firstT, impacto, normalizado)


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


def Refracciones(I, N, roiValue):
    firstE = 1
    EValue = roiValue
    factorIN = I @ N * -1
    if factorIN < 0:
        factorIN = factorIN * -1
        firstE = firstE * -1
        EValue = EValue * -1
        N = N * -1
    try:
        valueEt = firstE / EValue
    except:
        valueEt = 1

    valueEt2 = 1 - valueEt**2 * (1 - factorIN**2)
    if valueEt2 < 0:
        return V3(0, 0, 0)


class InterseccionXD:
    def __init__(self, distance, point, normal):
        self.distance = distance
        self.point = point
        self.normal = normal


"""
Class made to open an object from a file
"""


class ObjectOpener:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.glLines1()

    def glLines1(self):
        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
            except:
                continue
            if prefix == "v":
                self.vertices.append(list(map(float, value.split(" "))))
            elif prefix == "vt":
                self.texcoords.append(list(map(float, value.split(" "))))

            elif prefix == "f":
                self.faces.append(
                    [list(map(int, vert.split("/"))) for vert in value.split(" ")]
                )
