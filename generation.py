import random
from lxml import etree

import utils


def generate_background(options):
    """
    Fonction permettant d'ajouter un background
    :return: etree.Element
    """
    width = options.width
    height = options.height

    background_group = etree.Element('g')
    etree.SubElement(background_group, 'title').text = 'background'

    background = etree.SubElement(background_group, 'rect', id='background')
    background.set('x', '-1')
    background.set('y', '-1')
    background.set('width', str(width + 2))
    background.set('height', str(height + 2))

    background.set('fill', '#000000')

    return background_group


def generate_stars(options):
    """
    Fonction permettant d'ajouter des étoiles
    :return: etree.Element
    """
    width = options.width
    height = options.height
    color_palette = options.color_palette

    nb_stars = options.nb_stars
    min_size_stars = options.min_size_stars
    max_size_stars = options.max_size_stars
    color_proba = options.color_proba

    stars_group = etree.Element('g')
    etree.SubElement(stars_group, 'title').text = 'stars'

    for i in range(nb_stars):
        star_x = random.randint(0, width)
        star_y = random.randint(0, height)
        star_size = random.randint(min_size_stars, max_size_stars)

        star = etree.SubElement(stars_group, 'ellipse')
        star.set('cx', str(star_x))
        star.set('cy', str(star_y))
        star.set('rx', str(star_size))
        star.set('ry', str(star_size))

        if random.random() < color_proba:
            color = random.choice(color_palette)
        else:
            color = '#000000'

        star.set('fill', '{}'.format(color))
        star.set('stroke', 'none')
        star.set('fill-opacity', '{}'.format(random.random()))

    return stars_group


def generate_sun(options):
    """
    Fonction permettant de créer un soleil
    :return: etree.Element
    """
    height = options.height

    sun_size = int(height * 0.75)
    sun_x = int(height * (-0.358))
    sun_y = int(height / 2)

    #print(sun_size, sun_x, sun_y)  # Delete logs

    sun_group = etree.Element('g')
    etree.SubElement(sun_group, 'title').text = 'sun'
    sun = etree.SubElement(sun_group, 'ellipse', id='sun')

    sun.set('cx', str(sun_x))
    sun.set('cy', str(sun_y))
    sun.set('rx', str(sun_size))
    sun.set('ry', str(sun_size))

    sun.set('stroke-width', '2')
    sun.set('fill', '#000000')
    sun.set('stroke', '#ffffff')

    return sun_group, sun_x, sun_size


def generate_moons(planet_cx, options):

    height = options.height
    distance_moon = options.distance_moon

    moons = utils.random_size_moons(options)
    diff_pos_moon = utils.total_size_moons(moons, options)
    list_moons = []
    last_moon = ()

    cpt = 0
    for moo in moons:
        if cpt == 0:
            moon_value = planet_cx - diff_pos_moon
        else:
            moon_value = utils.new_pos_x(last_moon[0], last_moon[1], moo, distance_moon)

        moon = etree.Element('ellipse', id='moon_{}'.format(cpt))
        moon.set('cx', str(moon_value))
        moon.set('cy', str(0.75 * height))
        moon.set('rx', str(moo))
        moon.set('ry', str(moo))

        moon.set('fill', '#000000')
        moon.set('stroke', '#ffffff')
        moon.set('stroke-width', '2')

        list_moons.append(moon)
        last_moon = (moon_value, moo)
        cpt += 1

    return list_moons


def generate_rings(cx, cy, ray, options):

    min_ring = options.min_ring
    max_ring = options.max_ring

    rings = []
    nb_rings = random.randint(min_ring, max_ring)
    rotation_rings = random.randint(0, 360)

    for i in range(nb_rings):
        cpt = i * 5
        path = 'M{pos_x},{pos_y} a{distortion1},{distortion2} 0 1,0 {ray},0'.format(pos_x=cx - ray, pos_y=cy - cpt,
                                                                                    distortion1=(2 * ray) + cpt,
                                                                                    distortion2=15 + cpt,
                                                                                    ray=2 * ray)
        ring = etree.Element('path')
        ring.set('d', path)
        ring.set('fill', 'none')
        ring.set('stroke', '#ffffff')
        ring.set('stroke-width', '1.5')
        ring.set('transform', 'rotate({} {},{})'.format(rotation_rings, cx, cy))
        rings.append(ring)

    return rings


def generate_names(planet_cx, options):

    height = options.height
    font_size = options.font_size

    random_name = utils.random_name()
    planet_name = etree.Element('text', id='planet_name')

    planet_name.set('x', str(planet_cx))
    planet_name.set('y', str(0.90 * height))
    planet_name.set('font-family', 'Helvetica')
    planet_name.set('style', 'text-anchor: middle')
    planet_name.set('font-size', str(font_size))

    planet_name.set('fill-opacity', 'null')
    planet_name.set('fill', '#ffffff')
    planet_name.set('stroke-width', '0')

    planet_name.text = random_name

    return planet_name


def generate_planets(sun_pos_x, sun_size_r, options):

    height = options.height
    nb_planets = options.nb_planets
    min_size_planet = options.min_size_planet
    max_size_planet = options.max_size_planet
    distance_planet = options.distance_planet

    ring_proba = options.ring_proba
    moon_proba = options.moon_proba

    last_celestial = (sun_pos_x, sun_size_r)
    planets = []

    ls_seed = utils.split_str(options.id, nb_planets)

    for i in range(nb_planets):
        random.seed(ls_seed[i])
        random_size = random.randint(min_size_planet, max_size_planet)
        planet_x = utils.new_pos_x(last_celestial[0], last_celestial[1], random_size, distance_planet)
        planet_y = int(height / 2)

        # print(planet_x, planet_y)

        planet_group = etree.Element('g')
        etree.SubElement(planet_group, 'title').text = 'planet_{}'.format(i)
        planet = etree.SubElement(planet_group, 'ellipse', id='planet_{}'.format(i))

        planet.set('cx', str(planet_x))
        planet.set('cy', str(planet_y))
        planet.set('rx', str(random_size))
        planet.set('ry', str(random_size))

        planet.set('fill', '#000000')
        planet.set('stroke', '#ffffff')
        planet.set('stroke-width', '2')

        if random.random() < ring_proba:
            for ring_svg in generate_rings(planet_x, planet_y, random_size, options):  # Adding rings to planets
                planet_group.append(ring_svg)

        if random.random() < moon_proba:
            for moon_svg in generate_moons(planet_x, options):  # Adding moons to planets
                planet_group.append(moon_svg)

        planet_group.append(generate_names(planet_x, options))  # Adding name to planets

        planets.append(planet_group)
        last_celestial = (planet_x, random_size)

    return planets


def generate(options):

    width = options.width
    height = options.height

    background_svg = generate_background(options)
    stars_svg = generate_stars(options)
    sun_svg, sun_x, sun_size = generate_sun(options)
    planets_list_svg = generate_planets(sun_x, sun_size, options)

    root = etree.Element('svg', width=str(width), height=str(height), xmlns='http://www.w3.org/2000/svg')

    root.append(background_svg)
    root.append(stars_svg)
    root.append(sun_svg)

    for planet_svg in planets_list_svg:
        root.append(planet_svg)

    data = etree.tostring(root, pretty_print=True).decode('utf8')
    file_res = open(options.filename, 'w')
    file_res.write(data)
    file_res.close()
    print('SVG file saved : {}'.format(options.filename))
