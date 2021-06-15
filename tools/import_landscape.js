const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const yaml = require('js-yaml');

const csvIndexes = {
  isv: 0,
  platformVendor: 1,
  productName: 2,
  openSource: 3,
  partOfOdh: 4,
  communityOperator: 5,
  certifiedOperator: 6,
  ubiImplemented: 7,
  firstAiUseCase: 8,
  lastAiUseCase: 11,
  homepageUrl: 12,
  repoUrl: 13,
  logo: 14,
  twitter: 15,
  crunchbase: 16,
  componentProjects: 17,
  frameworks: 18,
  firstSubcategory: 27,
};

const args = process.argv;
const csvSource = args[2];
const ymlDest = args[3];

let csvRecords = [];
let landscape = [];
let categories = [];
let subcategories = [];

console.log(process.argv);
console.log(`Creating ${args[3]} from ${args[2]}`);

fs.createReadStream(csvSource).
  pipe(csv({headers: false})).
  on('data', data => csvRecords.push(data)).
  on('end', () => {
    writeYaml(csvRecords, ymlDest);
    outputInfo();
  });

function writeYaml(rows, ymlFile) {
  let isv;

  initLandscape(rows[0], rows[1]);
  for (let i = 2; i < rows.length; i++) {
    const row = rows[i];
    isv = row[0] ? row[0] : isv;
    processRow(isv, row);
  }

  finalizeLandscape();
  createYaml(ymlFile);
}

function outputInfo() {
  let frameworks = new Set();
  let frameworksFilter = new Set();
  let useCases = new Set();
  let useCasesFilter = new Set();
  landscape.forEach(category => {
    category.subcategories.forEach(subcategory => {
      if (subcategory.items) {
        subcategory.items.forEach(item => {
          if (item.frameworks_filter) {
            item.frameworks.split(',').
              map(s => s.trim()).
              filter(s => s && s.length > 0).
              forEach(f => frameworks.add(f));
            item.frameworks_filter.forEach(f => frameworksFilter.add(f));
          }
          if (item.use_cases_filter) {
            item.use_cases.split(',').
              map(s => s.trim()).
              filter(s => s && s.length > 0).
              forEach(f => useCases.add(f));
            item.use_cases_filter.forEach(uc => useCasesFilter.add(uc));
          }
        });
      }
    });
  });
  console.log('Add to Settings:');
  console.log('frameworks');
  console.log(frameworks);
  console.log(frameworksFilter);
  console.log('useCases');
  console.log(useCases);
  console.log(useCasesFilter);
}

function initLandscape(categoryRow, subcategoryRow) {
  let category, subcategory;
  let categoryArray = rowObjectToArray(categoryRow);
  let subcategoryArray = rowObjectToArray(subcategoryRow);
  landscape = [];

  for (let idx = 0; idx < subcategoryArray.length; idx++) {
    if (categoryArray[idx]) {
      category = {
        'category': null,
        'name': categoryArray[idx],
        'subcategories': [],
      };
      if (idx >= csvIndexes.firstSubcategory) {
        landscape.push(category);
      }
    }

    if (category && subcategoryArray[idx]) {
      subcategory = {
        'subcategory': null,
        'name': subcategoryArray[idx],
        'items': [],
      };
      category.subcategories.push(subcategory);
    }
    categories.push(category);
    subcategories.push(subcategory);
  }
  // console.log(landscape);
  // console.log(categories);
  // console.log(subcategories);
}

function processRow(isv, rowObject) {
  let rowArray = rowObjectToArray(rowObject);

  for (let idx = csvIndexes.firstSubcategory; idx < rowArray.length; idx++) {
    let value = rowArray[idx];
    if (value === 'FALSE') {
      continue;
    }

    addLandscapeItem(isv, rowArray, subcategories[idx]);
  }
}

function addLandscapeItem(isv, row, subcategory) {
  let product = row[csvIndexes.productName].trim();
  let openSource = row[csvIndexes.openSource].trim();
  let homepageUrl = row[csvIndexes.homepageUrl].trim() || 'missing-homepage';
  let repoUrl = row[csvIndexes.repoUrl].trim();
  let logo = row[csvIndexes.logo].trim() || 'no-image.svg';
  let twitter = row[csvIndexes.twitter].trim();
  let crunchbase = 'https://www.crunchbase.com/organization/no-data';
  let components = row[csvIndexes.componentProjects].trim();

  let name;
  if (!product || product.toLowerCase() === 'x' || product.toLowerCase() === isv.toLowerCase()) {
    name = `${isv} (${subcategory.name})`;
  } else if (product.toLowerCase().indexOf(isv.toLowerCase()) >= 0) {
    name = `${product} (${subcategory.name})`;
  } else {
    name = `${isv} ${product} (${subcategory.name})`;
  }

  let item = {
    'item': null,
    'organization': isv,
    'name': name,
    'homepage_url': homepageUrl,
    'open_source': openSource === 'full',
    'repo_url': repoUrl,
    'logo': logo,
    'twitter': twitter,
    'crunchbase': crunchbase,
    'components': components,
  };

  let status = getStatus(row);
  if (status && status.length > 0) {
    item.status = status;
  }

  let frameworks = row[csvIndexes.frameworks];
  let frameworksFilter = frameworks.split(',').
    map(s => s.trim().toLowerCase().replace(/\s/gi, '_')).
    filter(s => s && s.length > 0);
  if (frameworksFilter && frameworksFilter.length > 0) {
    item.frameworks = frameworks;
    item.frameworks_filter = frameworksFilter;
  }

  let {useCases, useCasesFilter} = getUseCases(row);
  if (useCasesFilter && useCasesFilter.length > 0) {
    item.use_cases = useCases;
    item.use_cases_filter = useCasesFilter;
  }

  if (repoUrl) {
    item['allow_duplicate_repo'] = true;
  }

  subcategory.items.push(item);
}

function getStatus(row) {
  let odh = row[csvIndexes.partOfOdh];
  let community = row[csvIndexes.communityOperator];
  let certified = row[csvIndexes.certifiedOperator];
  let ubi = row[csvIndexes.ubiImplemented];

  let status = [];
  if (odh === 'TRUE') {
    status.push('odh');
  }
  if (community === 'TRUE') {
    status.push('community');
  }
  if (certified === 'TRUE') {
    status.push('certified');
  }
  if (ubi === 'TRUE') {
    status.push('ubi');
  }

  return status;
}

function getUseCases(row) {
  const settings = [];
  for (let i = csvIndexes.firstAiUseCase; i <= csvIndexes.lastAiUseCase; i++) {
    settings.push({index: i, filterName: subcategories[i].name});
  }

  let {str, arr} = getFilter(settings, row);
  return {useCases: str, useCasesFilter: arr};
}

function getFilter(settings, row) {
  let filter = [];

  settings.forEach(x => {
    if (row[x.index] === 'TRUE') {
      filter.push(x.filterName);
    }
  });

  const str = filter.join(', ');
  const arr = filter.map(s => s.trim().toLowerCase().replace(/\s/gi, '_')).
    filter(s => s && s.length > 0);

  return {str, arr};
}

function finalizeLandscape() {
  const partnerCategory = {
    'category': null,
    'name': 'Open Data Hub Partner',
    'subcategories': [
      {
        'subcategory': null,
        'name': 'General',
        'items': [],
      },
    ],
  };

  landscape.push(partnerCategory);

  const hackCategory = {
    'category': null,
    'name': 'Hack',
    'subcategories': [
      {
        'subcategory': null,
        'name': 'Hack',
        'items': [
          {
            'item': null,
            'name': 'No Crunchbase Data Available',
            'homepage_url': 'https://www.no-data.com',
            'logo': 'no-data.svg',
            'crunchbase': 'https://www.crunchbase.com/organization/no-data',
          },
        ],
      },
    ],
  };

  landscape.push(hackCategory);
}

function createYaml(ymlFile) {
  let output = yaml.dump({landscape});

  // replace nulls with blank lines (why?)

  output = output.replace(/ null/g, '').replace(/''/g, 'null');

  fs.writeFileSync(ymlFile, output);
}

function rowObjectToArray(rowObject) {
  let rowArray = [];

  for (let [key, value] of Object.entries(rowObject)) {
    let idx = parseInt(key);

    if (isNaN(idx)) {
      continue;
    }

    rowArray[idx] = value;
  }

  return rowArray;
}
