-- specify database here
-- use Team_4;

drop table if exists clutch;
drop table if exists sort;
drop table if exists passage;

drop table if exists m_lines;
drop table if exists lab_members;

drop table if exists login_password;

create table m_lines( 
    l_id int not null auto_increment,
    yl_id char(6) not null,
    short_name varchar(100) not null,
    full_genotype varchar(100) not null,
    background varchar(100),
    published varchar(15),
    authors varchar(50),
    creators text,
    phenotype varchar(100),
    phenotype_notes text,
    genotype_notes text,
    dna_avail varchar(50),
    notes text,
    maintenance enum('Active', 'Retired') not null,
    primary key(l_id)
) engine = innodb;

create table lab_members(
    m_id int not null auto_increment,
    f_name varchar(100) not null,
    l_name varchar(100) not null,
    lab_role varchar(50),
    active enum('Active', 'Inactive'),
    primary key(m_id)
) engine = innodb;

create table passage(
    pass_id int not null auto_increment,
    l_id int not null,
    m_id int not null,

    bc int not null,
    ib int not null,
    hatch_date date not null,
    passage_date date not null,
    next_passage date not null,

    mating_line varchar(100),

    primary key(pass_id),
    index(l_id, pass_id),
    foreign key(l_id) references m_lines(l_id),
    foreign key(m_id) references lab_members(m_id)
) engine = innodb;

create table sort(
    sort_id int not null auto_increment,
    l_id int not null,
    m_id int not null,
    hatch_date date not null,
    sort_date date not null,
    
    line_name varchar(100) not null,
    marker_color varchar(50),
    marker_location varchar(100),
    fl_ratio float not null,
    fl_total int not null,
    notes text,

    primary key(sort_id),
    index(l_id, sort_id),
    foreign key(l_id) references m_lines(l_id),
    foreign key(m_id) references lab_members(m_id)
) engine = innodb;

create table clutch(
    clutch_id int not null auto_increment,
    l_id int not null,
    m_id int not null,

    hatch_date date not null,
    collection_date date not null,
    clutch_number int not null,
    egg_papers int not null,

    primary key(clutch_id),
    index(l_id, clutch_id),
    foreign key(l_id) references m_lines(l_id),
    foreign key(m_id) references lab_members(m_id)
) engine = innodb;

CREATE TABLE login_password(
    password_id int not null auto_increment,
    pass VARCHAR(255) not null,
    primary key(password_id)
) engine = innodb;
