
v0.2.0 / 2020-05-12
===================

  * Merge branch 'master' into dev
  * Merge pull request #1 from vartagg/master
  * Dockerizing; Postgis extension creation in first migration
  * Changed keys form to use the day instead of date
  * Add meta field to key item for metadata decryption
  * Group tracks by user key and day
  * Merge branch 'master' into dev
  * Fix day number<-> date conversion
  * Fix day number<-> date conversion
  * Create LICENSE
  * Update deploy fabfile
  * Update fabric
  * Remove tracks timestamp from query docs
  * Update latest swagger docs
  * Update README with latest links and deploy
  * Update README.md
  * Fix linter
  * Rename to oct-storage
  * Revise new format, remove security token, add boundary models and filters
  * Fix linter errors
  * Update API for keys and tracks with crypto keys
  * Add lastUpdateTimestamp to GET contacts, load contacts from contact_user_id
  * Add contacts endpoints

v0.1.0 / 2020-04-04
===================

  * Rename POST form timestamp->tst
  * Remove GET tracks fields
  * Flat point structure, make healthStatus non required
  * Add sentry integration
  * Revert timestamp filter, change created_from to lastUpdateTimestamp
  * Add created_from filter
  * Add timestamp filter in GET tracks
  * Update timestamp to milliseconds format
  * Change field names to camelCase
  * Update README.md
  * Update README.md
  * Add authentication by token
  * Add form validation, swagger api, change user id to int
  * Remove listing debug log
  * Update fab deploy script
  * Add ci and linter
  * Add track uploads
  * Initial commit
